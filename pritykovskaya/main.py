# coding=utf-8
__author__ = 'pritykovskaya'

import MySQLdb
import redis
import subprocess
import re
from subprocess import Popen, PIPE, STDOUT
from nltk.tokenize import wordpunct_tokenize
from collections import Counter


FILE_FOR_NORMALIZER = "file_for_normalizer"
FILE_FROM_NORMALIZER = "file_from_normalizer"

STOP_LIST_FILE = "stop_list"
NORMALIZER = "/home/pritykovskaya/PycharmProjects/prototype_find_good/normalizer.sh"

#utils
def read_stop_list():
    input = open(STOP_LIST_FILE, "r")
    stop_list = set()

    for line in input:
        stop_list.add(line.lower().rstrip())
    input.close()

    return stop_list
def parse_line(line):
    return map(lambda x: x.lower(), wordpunct_tokenize(line))

def filter_bag_of_words(bag, stop_list):
    return set(filter(lambda x: x not in stop_list, bag))

def normalize_bag_of_words(bag, norm_index):
    new_bag = set()
    for word in bag:
        if norm_index.exists(word):
            norm_word = norm_index.get(word)
            if norm_word != "":
                new_bag.add(norm_word)
        else: pass
    return new_bag

def parse_data(data, stop_list):
    word_bag = set()
    for rec in data:
        for text in rec[1:]:
            #print text
            word_bag |= set(parse_line(text)) #filter_bag_of_words(parse_line(text), stop_list)
    return word_bag

#create normalized index
def prepare_file_for_normalizer(word_bag):
    file_for_normalizer = open(FILE_FOR_NORMALIZER, "w")
    for word in word_bag:
        file_for_normalizer.write(word.encode('utf-8') + "\n")
    file_for_normalizer.close()
def call_normalizer():
    subprocess.call('cat '+ FILE_FOR_NORMALIZER + '|' + NORMALIZER + '>' + FILE_FROM_NORMALIZER , shell = True)
def redis_normal_index(redis):
    file_for_normalizer = open(FILE_FOR_NORMALIZER, "r")
    file_from_normalizer = open(FILE_FROM_NORMALIZER, "r")

    for pair in zip(file_for_normalizer, file_from_normalizer):
        #if pair[0].strip() != pair[1].strip():
            redis.set(pair[0].strip(), pair[1].strip())
        #print(pair[0].strip() +" " + pair[1].strip())
def create_normalized_index():
    db = connect_db()
    cursor = get_cursor(db)
    data = get_all_data_from_db(cursor)
    redis = redis_connect(0)

    stop_list = read_stop_list()
    prepare_file_for_normalizer(parse_data(data, stop_list))
    call_normalizer()
    redis_normal_index(redis)

# SQL stuff
def connect_db():
    # подключаемся к базе данных (не забываем указать кодировку, а то в базу запишутся иероглифы)
    db = MySQLdb.connect(host="localhost", user="root", passwd="booW1ham", db="goods_db", charset='utf8')
    return db
def get_cursor(db):
    cursor = db.cursor()
    return cursor
def get_all_data_from_db(cursor):
    # запрос к БД
    sql = """select * from items; """

    # выполняем запрос
    cursor.execute(sql)

    # получаем результат выполнения запроса
    data =  cursor.fetchall()
    return data
def disconnect_db(db):
    # закрываем соединение с БД
    db.close()

# redis stuff
def redis_connect(db_id):
    r = redis.StrictRedis(host='localhost', port=6379, db=db_id)
    return r

def create_indexes():
    db = connect_db()
    cursor = get_cursor(db)
    data = get_all_data_from_db(cursor)

    norm_redis = redis_connect(0)
    id_item_redis = redis_connect(1)
    word_ids_redis = redis_connect(2)
    idBag_length_redis = redis_connect(3)

    stop_list = read_stop_list()
    for rec in data:
        id = rec[0]
        name = rec[1]
        print str(id)  + " " + name
        id_item_redis.set(id, name)

        for i in range(1, 4):
            #print rec[i]
            cur_bag_of_words =  filter_bag_of_words(normalize_bag_of_words(parse_line(rec[i]), norm_redis),  stop_list)

            idBag_length_redis.set((id - 1)*3 + i - 1, len(cur_bag_of_words))

            for word in cur_bag_of_words:
                word_ids_redis.sadd(word, (id - 1)*3 + i - 1)

    disconnect_db(db)

def choose_keys_passed_threshold(id_freq, original_len):
    idBag_length_redis = redis_connect(3)

    dict_ids_passed_threshold = {}
    for key in id_freq.keys():
        inter_to_tag = id_freq[key]/float(original_len)
        inter_to_bagOfWord = id_freq[key]/float(idBag_length_redis.get(key))
        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = inter_to_tag + inter_to_bagOfWord
    return dict_ids_passed_threshold


def return_back_to_original_ids(dict_ids_passed_threshold):
    maxes = {}
    max_crit = 0
    for key in dict_ids_passed_threshold.keys():
        if dict_ids_passed_threshold[key] > max_crit:
            max_crit =  dict_ids_passed_threshold[key]
            maxes.clear()
            maxes[int(key)/3 + 1] = max_crit
        else:
            if dict_ids_passed_threshold[key] == max_crit:
                maxes[int(key)/3 + 1] = max_crit
    return maxes

def check_for_one_symbol_words(bag_of_words):
    for word in bag_of_words:
        if len(word) == 1:
            return True
    return False




def aggregate_tag(tag):
    stop_list = read_stop_list()

    # parse, normalize and filter tag
    cmd = 'echo '+ tag + '|' + NORMALIZER
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    bag_of_words = filter_bag_of_words(p.stdout.read().replace("\n", "").split("+"), stop_list)

    contain_one_symbol_words = check_for_one_symbol_words(bag_of_words)
    print contain_one_symbol_words

    original_len = len(bag_of_words)

    cur_ids = []

    id_item_redis = redis_connect(1)
    word_ids_redis = redis_connect(2)

    #find all bag ids, where words were mentioned
    for word in bag_of_words:
        cur_ids += word_ids_redis.smembers(word)

    #for each bag id count how many words it has
    id_freq = Counter(cur_ids)

    if not contain_one_symbol_words:
        bag_ids_passed_threshold = choose_keys_passed_threshold(id_freq, original_len)
        best_original_ids = return_back_to_original_ids(bag_ids_passed_threshold)
    else:
        #to do
        pass
    for id in best_original_ids.keys():
        print tag + "*" + id_item_redis.get(id) +"*" + str(id) + "*" + str(best_original_ids[id])


#create_normalized_index()
#create_indexes()



#key = "logitech"
#print r.smembers(key)

#key = r.randomkey()
#print key

aggregate_tag("000021 1 2 3 941 driving force gt logitech")
aggregate_tag("black ericsson mini sony st15i xperia")

#r = redis_connect(1)
#print r.get("8990")
#print r.get("8991")
#print r.get("8992")
#print r.get("8993")