# coding=utf-8
from redises import connect_word_to_bag_ids, connect_bag_id_to_length
from utils import is_one_symbol_word

__author__ = 'pritykovskaya'

class BaseSearcher(object):
    def __init__(self):
        self.bag_id_to_length_redis = connect_bag_id_to_length()
        self.word_to_bag_ids_redis = connect_word_to_bag_ids()

    # todo: разобрать специальный формат для написания комментариев
    # принимает тег в виде bag of words
    # возвращает bag ids
    # {bag_id : [intersection_size / tag_size, intersection_size / bag_size]}
    def find_bag_of_words_for_tag(self, bag_of_words):
        raise NotImplementedError()

    def is_above_thresholds(self, intersection_to_tag_ratio, intersection_to_bag_ratio):
        return intersection_to_tag_ratio >= 0.8 and intersection_to_bag_ratio >= 0.6

    def create_wordInfo_one_symbol_words(self, bag_of_words):
        id_wordsInfo = {}
        for word in bag_of_words:
            word_ids = self.word_to_bag_ids_redis.smembers(word)
            for id in word_ids:
                if id in id_wordsInfo:
                    id_wordsInfo[id][0] += 1
                    id_wordsInfo[id][1] += 1 if is_one_symbol_word(word) else 0
                else:
                    id_wordsInfo[id] = [1, 1 if is_one_symbol_word(word) else 0]
        return id_wordsInfo
