# coding=utf-8

from utils import *
from mysql_utils import *
from redis_utils import *
from normalizer import *

#create normalized index
def redis_normal_index(redis, words, normalized_words):
    for pair in zip(words, normalized_words):
        redis.set(pair[0].strip(), pair[1].strip())

def create_normalized_index():
    db = connect_db()
    cursor = db.cursor()
    data = get_all_data_from_db(cursor)
    redis = redis_connect(0)

    stop_list = read_stop_list(STOP_LIST_FILE)
    words = parse_data(data, stop_list)
    redis_normal_index(redis, words, normalize_bag_of_words(words))

def create_indexes():
    db = connect_db()
    cursor = db.cursor()
    data = get_all_data_from_db(cursor)

    norm_redis = redis_connect(0)
    id_item_redis = redis_connect(1)
    word_ids_redis = redis_connect(2)
    idBag_length_redis = redis_connect(3)

    idBag_bag = redis_connect(4)

    stop_list = read_stop_list(STOP_LIST_FILE)
    for rec in data:
        id = rec[0]
        name = rec[1]
        print str(id)  + " " + name
        id_item_redis.set(id, name)

        for i in range(1, 4):
            #print rec[i]
            cur_bag_of_words =  filter_bag_of_words(normalize_bag_of_words_with_index(parse_line(rec[i]), norm_redis),  stop_list)

            idBag_length_redis.set((id - 1)*3 + i - 1, len(cur_bag_of_words))
            idBag_bag.set((id - 1)*3 + i - 1, rec[i])

            for word in cur_bag_of_words:
                word_ids_redis.sadd(word, (id - 1)*3 + i - 1)

    disconnect_db(db)
