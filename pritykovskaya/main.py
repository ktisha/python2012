# coding=utf-8
__author__ = 'pritykovskaya'

import MySQLdb
import redis
import string

def import_items_from_db():
    # подключаемся к базе данных (не забываем указать кодировку, а то в базу запишутся иероглифы)
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="goods_db", charset='utf8')

    # формируем курсор, с помощью которого можно исполнять SQL-запросы
    cursor = db.cursor()

    # запрос к БД
    sql = """select * from items; """

    # выполняем запрос
    cursor.execute(sql)

    # получаем результат выполнения запроса
    data =  cursor.fetchall()
    items = {}

    # создаем свой словарь
    for rec in data:
        id, name, description, category = rec
        items[int(id)] = name
    # закрываем соединение с БД
    db.close()

    for key, value in items.iteritems():
        print (str(key) + "*" +value)

    return items

def export_items_in_redis(items):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for key, value in items.iteritems():
        r.set(key, value)
    print r.get('13735')

items = import_items_from_db()
export_items_in_redis(items)

