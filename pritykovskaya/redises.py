# coding=utf-8
import redis
import config

# как стоит делать: импортировать from config import * или только import config ?

def connect_word_to_norm_word():
    return __redis_connect(0)

def connect_id_to_item():
    return __redis_connect(1)

def connect_word_to_bag_ids():
    return __redis_connect(2)

def connect_bag_id_to_length():
    return __redis_connect(3)

def connect_bag_id_to_bag():
    return __redis_connect(4)

def __redis_connect(redis_id):
    r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=redis_id)
    return r