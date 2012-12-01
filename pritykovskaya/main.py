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
    #db = MySQLdb.connect(host="localhost", user="root", passwd="booW1ham", db="goods_db", charset='utf8')
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="goods_db_with_cats", charset='utf8')
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
    counter = 0
    for word in bag_of_words:
        if len(word) == 1:
            counter += 1
    return counter

#добавить полиморфизм

# to do
# если tag пересекается только с категорией (mod key 3 == 2)
# то это не зачет
# если tag пересекается с 2мя товарами, то
# c одинаковым порогами, то
# начинает играть роль в каком товаре он пересекся с большим количеством сущностей


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

# todo
# description следует рассматривать с другим порогом
# например, если весь тег лежит в description - все
# супер

def intersected_only_with_cat(triplet):
    if triplet[0] == 0 and triplet[1] == 0:
        return True
    else:
        return False

def return_back_to_original_ids_filter_categories(dict_ids_passed_threshold):
    my_dict = {}
    for key in dict_ids_passed_threshold.keys():
        if int(key)/3 + 1 not in my_dict.keys():
            my_dict[int(key)/3 + 1] = [0, 0, 0]
            my_dict[int(key)/3 + 1][int(key) % 3] = dict_ids_passed_threshold[key]
        else:
            my_dict[int(key)/3 + 1][int(key) % 3] = dict_ids_passed_threshold[key]

    # should choose best sum and mentioned if tag intersected only with cat
    max = 0
    best_ids = {}
    for key in my_dict:
        if sum(my_dict[key]) > max:
            max = sum(my_dict[key])
            best_ids.clear()
            best_ids[key] = [max, intersected_only_with_cat(my_dict[key])]
        else:
            if sum(my_dict[key]) == max:
                best_ids[key] = [max, intersected_only_with_cat(my_dict[key])]
    return best_ids



def check_if_one_symbol_word(word):
    if len(word) == 1:
        return 1
    else:
        return 0

def create_wordInfo_one_symbol_words(bag_of_words, word_ids_redis):
    id_wordsInfo = {}
    for word in bag_of_words:
        is_one_word = check_if_one_symbol_word(word)
        word_ids = word_ids_redis.smembers(word)
        for id in word_ids:
            if id in id_wordsInfo:
                id_wordsInfo[id][0] += 1
                id_wordsInfo[id][1] += is_one_word
            else:
                id_wordsInfo[id] = [1, is_one_word]
    return id_wordsInfo

def choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len):
    idBag_length_redis = redis_connect(3)

    dict_ids_passed_threshold = {}
    for key in id_wordsInfo.keys():
        # прибавляем к длине тега (без односимвольных слов)
        # количество односимвольных слов, которые
        # лежат в рассматриваемом листе

        actual_original_len = original_len + id_wordsInfo[key][1]

        inter_to_tag = id_wordsInfo[key][0]/float(actual_original_len)
        inter_to_bagOfWord = id_wordsInfo[key][0]/float(idBag_length_redis.get(key))

        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = inter_to_tag + inter_to_bagOfWord
    return dict_ids_passed_threshold

def find_items_for_tag(bag_of_words):
    number_of_one_symbol_words = check_for_one_symbol_words(bag_of_words)
    print number_of_one_symbol_words

    original_len = len(bag_of_words) - number_of_one_symbol_words
    word_ids_redis = redis_connect(2)


    if number_of_one_symbol_words == 0:
        cur_ids = []
        #find all bag ids, where words were mentioned
        for word in bag_of_words:
            cur_ids += word_ids_redis.smembers(word)

        #for each bag id count how many words it has
        id_freq = Counter(cur_ids)

        bag_ids_passed_threshold = choose_keys_passed_threshold(id_freq, original_len)
    else:
        id_wordsInfo = create_wordInfo_one_symbol_words(bag_of_words, word_ids_redis)
        bag_ids_passed_threshold = choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len)

    #best_original_ids = return_back_to_original_ids(bag_ids_passed_threshold)
    best_original_ids = return_back_to_original_ids_filter_categories(bag_ids_passed_threshold)
    return best_original_ids

def aggregate_tag(tag):
    stop_list = read_stop_list()

    # parse, normalize and filter tag
    cmd = 'echo '+ tag + '|' + NORMALIZER
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    bag_of_words = filter_bag_of_words(p.stdout.read().replace("\n", "").split("+"), stop_list)

    # link tag and items
    best_original_ids = find_items_for_tag(bag_of_words)
    print (best_original_ids)

    id_item_redis = redis_connect(1)

    if len(best_original_ids) == 0:
        #trying to cut kirillic letters and start again
        bag_of_words = filter_cyrillic(bag_of_words)
        best_original_ids = find_items_for_tag(bag_of_words)
        print (best_original_ids)

    for id in best_original_ids.keys():
        print tag + "*" + id_item_redis.get(id) +"*" + str(id) + "*" + str(best_original_ids[id][0]) \
                                                                + "*" + str(best_original_ids[id][1])



def contain_only_ascii(word):
    if re.match("^[A-Za-z0-9]+$", word):
        return word

def filter_cyrillic(bag_of_words):
    return filter(lambda x: contain_only_ascii(x), bag_of_words)

#create_normalized_index()
#create_indexes()



#key = "logitech"
#print r.smembers(key)

#key = r.randomkey()
#print key

#aggregate_tag("ежики мылились 1 1 1 3 4 5")
#aggregate_tag("000021 1 2 3 941 driving force gt logitech")
#aggregate_tag("black ericsson mini sony st15i xperia")
#aggregate_tag("Стильный и функциональный пылесос от известного производителя!")
#aggregate_tag("Пылесосы и пылесборники")
#aggregate_tag("nikon Coolpix S8200")
#aggregate_tag("8 blackbox xdevice видеорегистратор")
#aggregate_tag("325 clp")
#aggregate_tag("galaxy gt i9001 plus s samsung отзыв")
#aggregate_tag("oregon scientific")
#r = redis_connect(1)
#print r.get("8990")
#print r.get("8991")
#print r.get("8992")
#print r.get("8993")

aggregate_tag("galaxy gt i9001 plus s samsung отзыв")
f = open("example", "r")
for line in f:
    aggregate_tag(line.strip())

f.close()

#todo:
# добавить список брендов
# добавить проверку есть ли только цифры в пересечении
# добавить проверку есть код в пересечении

# подумать на делеммой искать и в категории vs
# искать только в описании и имени, и если не нашлось,
# то в категории, собрать соотв статистику

# написать тест 
# для этого сделать вывод того, с чем пересеклось
