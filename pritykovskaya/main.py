# coding=utf-8
__author__ = 'pritykovskaya'

import MySQLdb
import redis
import re
import sys
from nltk.tokenize import wordpunct_tokenize

FILE_FOR_NORMALIZER = "file_for_normalizer"
FILE_FROM_NORMALIZER = "file_from_normalizer"

STOP_LIST_FILE = "stoplist"
PATH_TO_NORMALIZER = ""


def read_stop_list():
    input = open(STOP_LIST_FILE, "r")
    stop_list = set()

    for line in input:
        stop_list.add(line.lower().rstrip())

    return stop_list


def parse_line(line):
    return set(map(lambda x: x.lower(), wordpunct_tokenize(line)))

def parse_data(data, stop_list):
    word_bag = set()
    for rec in data:
        for text in rec[1:]:
            print text
            word_bag |= parse_line(text)
    return word_bag


def normalize(word_bag):

    file_for_normalizer = open(FILE_FOR_NORMALIZER, "w")
    for word in word_bag:
        file_for_normalizer.write(word.encode('utf-8') + "\n")
    file_for_normalizer.close()

    # launch normalizer
    # to do


def redis_normal_index(redis):
    file_for_normalizer = open(FILE_FOR_NORMALIZER, "r")
    file_from_normalizer = open(FILE_FROM_NORMALIZER, "r")

    for pair in zip(file_for_normalizer, file_from_normalizer):
        redis.set(pair[0].strip(), pair[1].strip())
        print(pair[0].strip() +" " + pair[1].strip())
def create_normalized_index(data, redis):
    #stop_list = read_stop_list(sys.argv[1])

    stop_list = set()
    normalize(parse_data(data, stop_list))
    #redis_normal_index(redis)

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

def import_items_from_db():
    items = {}
    db = connect_db()
    cursor = get_cursor(db)
    data = get_all_data_from_db(cursor)
    #create_normalized_index(data, redis)

    for rec in data:
        id, name, descr, cat = rec
        items[id] = name

    #for key, value in items.iteritems():
        #print (str(key) + "*" +value)

    disconnect_db(db)
    return items

def create_back_index():
    pass


def redis_connect():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r

def export_items_in_redis(items, r):

    my_dict = {}

    for id, name in items.iteritems():
        words = name.split(" ")
        for word in words:
            if word in my_dict.keys():
                my_dict[word].add(id)
            else:
                my_dict[word]=set()
                my_dict[word].add(id)
            r.sadd(word, id)

    print (r.scard("Passport"))
    print my_dict["Passport"]

db = connect_db()
cursor = get_cursor(db)
data = get_all_data_from_db(cursor)
redis = redis_connect()

create_normalized_index(data, redis)
#redis_normal_index(redis)

#print(redis.get("правильную"))
#print(redis.get("складывается"))
#print(redis.get("."))
#print(redis.get("!"))
#items = import_items_from_db()
#export_items_in_redis(items, redis)

