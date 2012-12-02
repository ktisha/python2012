# coding=utf-8
from collections import Counter
from searcher.BaseSearcher import BaseSearcher
from utils import *

class TestSearcher(BaseSearcher):
    def __init__(self):
        BaseSearcher.__init__(self)

    def find_bag_of_words_for_tag(self, bag_of_words):
        number_of_one_symbol_words = count_one_symbol_words(bag_of_words)
        #print number_of_one_symbol_words

        original_len = len(bag_of_words) - number_of_one_symbol_words
        #original_len = len(bag_of_words)

        if number_of_one_symbol_words == 0:

            cur_ids = []
            #find all bag ids, where words were mentioned
            for word in bag_of_words:
                cur_ids += self.WORD_IDS.smembers(word)

            #for each bag id count how many words it has
            id_freq = Counter(cur_ids)
            if len(id_freq) != 0:
                bag_ids_passed_threshold = self.choose_keys_passed_threshold_for_test(id_freq, original_len)
                return bag_ids_passed_threshold
            else: return set()
        else:
            id_wordsInfo = self.create_wordInfo_one_symbol_words(bag_of_words)
            bag_ids_passed_threshold = self.choose_keys_passed_threshold_with_one_symbol_words_for_test(id_wordsInfo, original_len)
            return bag_ids_passed_threshold

    def choose_keys_passed_threshold_for_test(self, id_freq, original_len):
        dict_ids_passed_threshold = {}
        for key in id_freq.keys():
            inter_to_tag = id_freq[key]/float(original_len)
            inter_to_bagOfWord = id_freq[key]/float(self.IDBAG_LENGTH.get(key))
            if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
                dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
        return dict_ids_passed_threshold

    def choose_keys_passed_threshold_with_one_symbol_words_for_test(self, id_wordsInfo, original_len):
        dict_ids_passed_threshold = {}
        for key in id_wordsInfo.keys():
            # прибавляем к длине тега (без односимвольных слов)
            # количество односимвольных слов, которые
            # лежат в рассматриваемом листе

            actual_original_len = original_len + id_wordsInfo[key][1]

            inter_to_tag = id_wordsInfo[key][0]/float(actual_original_len)
            inter_to_bagOfWord = id_wordsInfo[key][0]/float(self.IDBAG_LENGTH.get(key))

            if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
                dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
        return dict_ids_passed_threshold
