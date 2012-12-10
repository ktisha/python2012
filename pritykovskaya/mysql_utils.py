# coding=utf-8
import _mysql_exceptions

from config import *
import MySQLdb

GOODS_DB="goods_db_with_cats"
# MYSQL_DB="goods_db"

# SQL stuff
def connect_db():
    # подключаемся к базе данных (не забываем указать кодировку, а то в базу запишутся иероглифы)
    try:
        db = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=GOODS_DB, charset=MYSQL_CHARSET)
    except _mysql_exceptions.OperationalError:
        print("No connection to MySql. Check config.py")
        exit(1)
    else:
        return db


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