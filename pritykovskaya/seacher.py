# coding=utf-8
from redises import *
from utils import *
from collections import Counter

IDBAG_LENGTH = connect_bag_id_to_length()
WORD_IDS = connect_word_to_bag_ids()

#добавить полиморфизм
def choose_keys_passed_threshold(id_freq, original_len):
    idBag_length_redis = IDBAG_LENGTH

    dict_ids_passed_threshold = {}
    for key in id_freq.keys():
        inter_to_tag = id_freq[key]/float(original_len)
        inter_to_bagOfWord = id_freq[key]/float(idBag_length_redis.get(key))
        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = inter_to_tag + inter_to_bagOfWord
    return dict_ids_passed_threshold
def choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len):
    idBag_length_redis = IDBAG_LENGTH

    dict_ids_passed_threshold = {}
    for key in id_wordsInfo.keys():
        # прибавляем к длине тега (без односимвольных слов)
        # количество односимвольных слов, которые
        # лежат в рассматриваемом листе

        actual_original_len = original_len + id_wordsInfo[key][1]

        inter_to_tag = id_wordsInfo[key][0]/float(actual_original_len)
        inter_to_bagOfWord = id_wordsInfo[key][0]/float(idBag_length_redis.get(key))

        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = inter_to_tag + inter_to_bagOfWord
    return dict_ids_passed_threshold

def create_wordInfo_one_symbol_words(bag_of_words):
    id_wordsInfo = {}
    for word in bag_of_words:
        word_ids = WORD_IDS.smembers(word)
        for id in word_ids:
            if id in id_wordsInfo:
                id_wordsInfo[id][0] += 1
                id_wordsInfo[id][1] += 1 if is_one_symbol_word(word) else 0
            else:
                id_wordsInfo[id] = [1, 1 if is_one_symbol_word(word) else 0]
    return id_wordsInfo


# to do
# если tag пересекается только с категорией (mod key 3 == 2)
# то это не зачет
# если tag пересекается с 2мя товарами, то
# c одинаковым порогами, то
# начинает играть роль в каком товаре он пересекся с большим количеством сущностей

# todo: разобрать специальный формат для написания комментариев
# принимает тег в виде bag of words
# возвращает bag ids
def find_bag_of_words_for_tag(bag_of_words):
    number_of_one_symbol_words = count_one_symbol_words(bag_of_words)
    print number_of_one_symbol_words

    original_len = len(bag_of_words) - number_of_one_symbol_words
    word_ids_redis = WORD_IDS


    if number_of_one_symbol_words == 0:
        cur_ids = []
        #find all bag ids, where words were mentioned
        for word in bag_of_words:
            cur_ids += word_ids_redis.smembers(word)

        #for each bag id count how many words it has
        id_freq = Counter(cur_ids)

        bag_ids_passed_threshold = choose_keys_passed_threshold(id_freq, original_len)
    else:
        id_wordsInfo = create_wordInfo_one_symbol_words(bag_of_words)
        bag_ids_passed_threshold = choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len)

    return bag_ids_passed_threshold

def choose_keys_passed_threshold_for_test(id_freq, original_len):

    dict_ids_passed_threshold = {}
    for key in id_freq.keys():
        inter_to_tag = id_freq[key]/float(original_len)
        inter_to_bagOfWord = id_freq[key]/float(IDBAG_LENGTH.get(key))
        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
    return dict_ids_passed_threshold

def choose_keys_passed_threshold_with_one_symbol_words_for_test(id_wordsInfo, original_len):

    dict_ids_passed_threshold = {}
    for key in id_wordsInfo.keys():
        # прибавляем к длине тега (без односимвольных слов)
        # количество односимвольных слов, которые
        # лежат в рассматриваемом листе

        actual_original_len = original_len + id_wordsInfo[key][1]

        inter_to_tag = id_wordsInfo[key][0]/float(actual_original_len)
        inter_to_bagOfWord = id_wordsInfo[key][0]/float(IDBAG_LENGTH.get(key))

        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = [inter_to_tag, inter_to_bagOfWord]
    return dict_ids_passed_threshold

def find_items_for_tag_for_test(bag_of_words):
    number_of_one_symbol_words = count_one_symbol_words(bag_of_words)
    #print number_of_one_symbol_words

    original_len = len(bag_of_words) - number_of_one_symbol_words
    #original_len = len(bag_of_words)

    if number_of_one_symbol_words == 0:

        cur_ids = []
        #find all bag ids, where words were mentioned
        for word in bag_of_words:
            cur_ids += WORD_IDS.smembers(word)

        #for each bag id count how many words it has
        id_freq = Counter(cur_ids)
        if len(id_freq) != 0:
            bag_ids_passed_threshold = choose_keys_passed_threshold_for_test(id_freq, original_len)
            return bag_ids_passed_threshold
        else: return set()
    else:
        id_wordsInfo = create_wordInfo_one_symbol_words(bag_of_words)
        bag_ids_passed_threshold = choose_keys_passed_threshold_with_one_symbol_words_for_test(id_wordsInfo, original_len)
        return bag_ids_passed_threshold
