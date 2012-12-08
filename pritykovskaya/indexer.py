# coding=utf-8

from common import *
from mysql_utils import *
from redises import *
from normalizer import *

#create normalized index
from utils import parse_data, filter_bag_of_words, normalize_bag_of_words_with_index, parse_line

def redis_normal_index(redis, words, normalized_words):
    for pair in zip(words, normalized_words):
        redis.set(pair[0].strip(), pair[1].strip())

def create_normalized_index():
    db = connect_db()
    cursor = db.cursor()
    data = get_all_data_from_db(cursor)
    redis = connect_word_to_norm_word()

    words = parse_data(data)
    redis_normal_index(redis, words, normalize_bag_of_words(words))

def create_indexes():
    db = connect_db()
    cursor = db.cursor()
    data = get_all_data_from_db(cursor)

    norm_redis = connect_word_to_norm_word()
    id_item_redis = connect_id_to_item()
    word_ids_redis = connect_word_to_bag_ids()
    word_ids_redis_quick = connect_word_to_bag_ids_quick()
    idBag_length_redis = connect_bag_id_to_length()

    idBag_bag = connect_bag_id_to_bag()

    for rec in data:
        item_id = rec[0]
        name = rec[1]
        print str(item_id)  + " " + name
        id_item_redis.set(item_id, name)

        for i in range(1, 4):
            #print rec[i]
            cur_bag_of_words =  filter_bag_of_words(normalize_bag_of_words_with_index(parse_line(rec[i]), norm_redis), STOP_LIST)

            idBag_length_redis.set((item_id - 1)*3 + i - 1, len(cur_bag_of_words))
            idBag_bag.set((item_id - 1)*3 + i - 1, rec[i])

            for word in cur_bag_of_words:
                word_ids_redis.sadd(word, (item_id - 1)*3 + i - 1)
                word_ids_redis_quick.zadd(word, 1, (item_id - 1)*3 + i - 1)

    disconnect_db(db)
