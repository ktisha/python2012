# coding=utf-8
import redis
import config

# как стоит делать: импортировать from config import * или только import config ?

def redis_connect(redis_id):
    r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=redis_id)
    return r
