# coding=utf-8
import redis
from redises import connect_word_to_bag_ids, connect_bag_id_to_length, connect_word_to_bag_ids_quick
from utils import is_one_symbol_word

__author__ = 'pritykovskaya'

class BaseSearcher(object):
    def __init__(self):
        self.bag_id_to_length_redis = connect_bag_id_to_length()
        self.word_to_bag_ids_redis = connect_word_to_bag_ids()
        self.word_to_bag_ids_redis_quick = connect_word_to_bag_ids_quick()

    # todo: разобрать специальный формат для написания комментариев
    # принимает тег в виде bag. of words
    # возвращает bag ids
    # {bag_id : [intersection_size / tag_size, intersection_size / bag_size]}
    def find_bag_of_words_for_tag(self, bag_of_words):
        raise NotImplementedError()

    def is_above_thresholds(self, intersection_to_tag_ratio, intersection_to_bag_ratio):
        return intersection_to_tag_ratio >= 0.8 and intersection_to_bag_ratio >= 0.6

    def create_wordInfo_one_symbol_words(self, bag_of_words, candidates):
        raise NotImplementedError()

    def choose_keys_passed_threshold_with_one_symbol_words(self, id_wordsInfo, original_len):
        dict_ids_passed_threshold = {}
        for key in id_wordsInfo.keys():
            # прибавляем к длине тега (без односимвольных слов)
            # количество односимвольных слов, которые
            # лежат в рассматриваемом листе
            actual_original_len = original_len + id_wordsInfo[key][1]
            if actual_original_len != 0 :
                inter_to_tag = id_wordsInfo[key][0]/float(actual_original_len)
                inter_to_bagOfWord = id_wordsInfo[key][0]/float(self.bag_id_to_length_redis.get(key))

                if self.is_above_thresholds(inter_to_tag, inter_to_bagOfWord):
                    dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
        return dict_ids_passed_threshold
