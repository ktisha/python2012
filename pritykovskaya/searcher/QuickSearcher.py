# coding=utf-8
from searcher.BaseSearcher import BaseSearcher
from utils import *
from collections import Counter
import math

class QuickSearcher(BaseSearcher):
    def __init__(self):
        BaseSearcher.__init__(self)

    def choose_keys_passed_threshold(self, original_len):
        dict_ids_passed_threshold = {}
        # count boundary
        boundary = math.ceil(float(original_len) * 0.8)
        candidates = self.word_to_bag_ids_redis_quick.zrangebyscore("union", boundary, "+inf", withscores=True)

        for candidate in candidates:
            candidate_id = candidate[0]
            volume_of_intersection = candidate[1]
            inter_to_bagOfWord = volume_of_intersection/float(self.bag_id_to_length_redis.get(candidate_id))

            if inter_to_bagOfWord >= 0.6:
                dict_ids_passed_threshold[candidate_id] = [int(candidate[1])/float(original_len), inter_to_bagOfWord]
        return dict_ids_passed_threshold
    def create_wordInfo_one_symbol_words(self, bag_of_words, candidates):
        id_wordsInfo = {}
        # идем по всем словам тега
        for word in bag_of_words:
            is_one_word = is_one_symbol_word(word)
            # идем по всем кандидатам на товар
            # если слово однословное, то должны проверить,
            # входит ли оно в данного кандидата
            word_ids = self.word_to_bag_ids_redis.smembers(word)
            for candidate_id in candidates:
                if candidate_id[0] in id_wordsInfo:
                    id_wordsInfo[candidate_id[0]][1] += check_link_between_word_and_item(candidate_id, word_ids)
                else:
                    id_wordsInfo[candidate_id[0]] = [candidate_id[1], check_link_between_word_and_item(candidate_id, word_ids)]
        return id_wordsInfo
    def find_bag_of_words_for_tag(self, bag_of_words):
        bag_ids_passed_threshold = {}
        if len(bag_of_words) != 0:

            number_of_one_symbol_words = count_one_symbol_words(bag_of_words)
            original_len = len(bag_of_words) - number_of_one_symbol_words
            #original_len = len(bag_of_words)
            self.word_to_bag_ids_redis_quick.zunionstore("union", bag_of_words)

            if number_of_one_symbol_words == 0:
                cur_ids = []
                #find all bag ids, where words were mentioned
                #for each bag id count how many words it has
                if self.word_to_bag_ids_redis_quick.zcard("union") != 0:
                    bag_ids_passed_threshold = self.choose_keys_passed_threshold(original_len)
            else:
                boundary = math.ceil(float(original_len) * 0.8)
                candidates = self.word_to_bag_ids_redis_quick.zrangebyscore("union", boundary, "+inf", withscores=True)

                id_wordsInfo = self.create_wordInfo_one_symbol_words(bag_of_words, candidates)
                bag_ids_passed_threshold = self.choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len)

        return bag_ids_passed_threshold



# todo
# если tag пересекается только с категорией (mod key 3 == 2)
# то это не зачет
# если tag пересекается с 2мя товарами, то
# c одинаковым порогами, то
# начинает играть роль в каком товаре он пересекся с большим количеством сущностей

