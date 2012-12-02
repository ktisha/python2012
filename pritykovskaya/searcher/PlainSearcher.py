# coding=utf-8
from searcher.BaseSearcher import BaseSearcher
from utils import *
from collections import Counter

class PlainSearcher(BaseSearcher):
    def __init__(self):
        BaseSearcher.__init__(self)

    def find_bag_of_words_for_tag(self, bag_of_words):
        number_of_one_symbol_words = count_one_symbol_words(bag_of_words)
        original_len = len(bag_of_words) - number_of_one_symbol_words
        # print number_of_one_symbol_words
        bag_ids_passed_threshold = set()

        if number_of_one_symbol_words == 0:
            cur_ids = []
            #find all bag ids, where words were mentioned
            for word in bag_of_words:
                cur_ids += self.word_to_bag_ids_redis.smembers(word)

            #for each bag id count how many words from tag it has
            if len(cur_ids) != 0:
                id_freq = Counter(cur_ids)
                bag_ids_passed_threshold = self.choose_keys_passed_threshold(id_freq, original_len)
        else:
            id_wordsInfo = self.create_wordInfo_one_symbol_words(bag_of_words)
            bag_ids_passed_threshold = self.choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len)

        return bag_ids_passed_threshold

    def choose_keys_passed_threshold(self, id_freq, original_len):
        dict_ids_passed_threshold = {}
        for key in id_freq.keys():
            inter_to_tag = id_freq[key]/float(original_len)
            inter_to_bagOfWord = id_freq[key]/float(self.bag_id_to_length_redis.get(key))
            if self.is_above_thresholds(inter_to_tag, inter_to_bagOfWord):
                dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
        return dict_ids_passed_threshold

    def choose_keys_passed_threshold_with_one_symbol_words(self, id_wordsInfo, original_len):
        dict_ids_passed_threshold = {}
        for key in id_wordsInfo.keys():
            # прибавляем к длине тега (без односимвольных слов)
            # количество односимвольных слов, которые
            # лежат в рассматриваемом листе
            actual_original_len = original_len + id_wordsInfo[key][1]

            inter_to_tag = id_wordsInfo[key][0]/float(actual_original_len)
            inter_to_bagOfWord = id_wordsInfo[key][0]/float(self.bag_id_to_length_redis.get(key))

            if self.is_above_thresholds(inter_to_tag, inter_to_bagOfWord):
                dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
        return dict_ids_passed_threshold

# todo
# если tag пересекается только с категорией (mod key 3 == 2)
# то это не зачет
# если tag пересекается с 2мя товарами, то
# c одинаковым порогами, то
# начинает играть роль в каком товаре он пересекся с большим количеством сущностей
