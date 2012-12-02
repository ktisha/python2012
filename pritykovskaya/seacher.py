# coding=utf-8
from config import STOP_LIST_FILE
from normalizer import normalize_tag
from redises import *
from utils import check_if_one_symbol_word, read_stop_list, filter_bag_of_words, filter_cyrillic
from collections import Counter

IDBAG_LENGTH = connect_bag_id_to_length()
IDBAG_BAG = connect_bag_id_to_bag()
WORD_IDS = connect_word_to_bag_ids()
ID_TO_ITEM_REDIS = connect_id_to_item()

def choose_keys_passed_threshold(id_freq, original_len):
    idBag_length_redis = IDBAG_LENGTH

    dict_ids_passed_threshold = {}
    for key in id_freq.keys():
        inter_to_tag = id_freq[key]/float(original_len)
        inter_to_bagOfWord = id_freq[key]/float(idBag_length_redis.get(key))
        if inter_to_tag >= 0.8 and inter_to_bagOfWord >= 0.6:
            dict_ids_passed_threshold[key] = inter_to_tag + inter_to_bagOfWord
    return dict_ids_passed_threshold

def return_back_to_original_ids(dict_ids_passed_threshold):
    maxes = {}
    max_crit = 0
    for key in dict_ids_passed_threshold.keys():
        if dict_ids_passed_threshold[key] > max_crit:
            max_crit =  dict_ids_passed_threshold[key]
            maxes.clear()
            maxes[int(key)/3 + 1] = max_crit
        else:
            if dict_ids_passed_threshold[key] == max_crit:
                maxes[int(key)/3 + 1] = max_crit
    return maxes

def check_for_one_symbol_words(bag_of_words):
    counter = 0
    for word in bag_of_words:
        if len(word) == 1:
            counter += 1
    return counter

#добавить полиморфизм

# to do
# если tag пересекается только с категорией (mod key 3 == 2)
# то это не зачет
# если tag пересекается с 2мя товарами, то
# c одинаковым порогами, то
# начинает играть роль в каком товаре он пересекся с большим количеством сущностей

def return_back_to_original_ids(dict_ids_passed_threshold):
    maxes = {}
    max_crit = 0
    for key in dict_ids_passed_threshold.keys():
        if dict_ids_passed_threshold[key] > max_crit:
            max_crit =  dict_ids_passed_threshold[key]
            maxes.clear()
            maxes[int(key)/3 + 1] = max_crit
        else:
            if dict_ids_passed_threshold[key] == max_crit:
                maxes[int(key)/3 + 1] = max_crit
    return maxes

def intersected_only_with_cat(triplet):
    if triplet[0] == 0 and triplet[1] == 0:
        return True
    else:
        return False

def return_back_to_original_ids_filter_categories(dict_ids_passed_threshold):
    my_dict = {}
    for key in dict_ids_passed_threshold.keys():
        if int(key)/3 + 1 not in my_dict.keys():
            my_dict[int(key)/3 + 1] = [0, 0, 0]
            my_dict[int(key)/3 + 1][int(key) % 3] = dict_ids_passed_threshold[key]
        else:
            my_dict[int(key)/3 + 1][int(key) % 3] = dict_ids_passed_threshold[key]

    # should choose best sum and mentioned if tag intersected only with cat
    max = 0
    best_ids = {}
    for key in my_dict:
        if sum(my_dict[key]) > max:
            max = sum(my_dict[key])
            best_ids.clear()
            best_ids[key] = [max, intersected_only_with_cat(my_dict[key])]
        else:
            if sum(my_dict[key]) == max:
                best_ids[key] = [max, intersected_only_with_cat(my_dict[key])]
    return best_ids

def create_wordInfo_one_symbol_words(bag_of_words):
    id_wordsInfo = {}
    for word in bag_of_words:
        is_one_word = check_if_one_symbol_word(word)
        word_ids = WORD_IDS.smembers(word)
        for id in word_ids:
            if id in id_wordsInfo:
                id_wordsInfo[id][0] += 1
                id_wordsInfo[id][1] += is_one_word
            else:
                id_wordsInfo[id] = [1, is_one_word]
    return id_wordsInfo

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

def find_items_for_tag(bag_of_words):
    number_of_one_symbol_words = check_for_one_symbol_words(bag_of_words)
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
        id_wordsInfo = create_wordInfo_one_symbol_words(bag_of_words, word_ids_redis)
        bag_ids_passed_threshold = choose_keys_passed_threshold_with_one_symbol_words(id_wordsInfo, original_len)

    #best_original_ids = return_back_to_original_ids(bag_ids_passed_threshold)
    best_original_ids = return_back_to_original_ids_filter_categories(bag_ids_passed_threshold)
    return best_original_ids

def aggregate_tag(tag):
    stop_list = read_stop_list(STOP_LIST_FILE)

    # parse, normalize and filter tag
    # normalize
    bag_of_words = filter_bag_of_words(normalize_tag(tag).replace("\n", "").split("+"), stop_list)

    # link tag and items
    best_original_ids = find_items_for_tag(bag_of_words)
    print (best_original_ids)

    id_item_redis = ID_TO_ITEM_REDIS

    if len(best_original_ids) == 0:
        #trying to cut kirillic letters and start again
        bag_of_words = filter_cyrillic(bag_of_words)
        best_original_ids = find_items_for_tag(bag_of_words)
        print (best_original_ids)

    for id in best_original_ids.keys():
        print tag + "*" + id_item_redis.get(id) +"*" + str(id) + "*" + str(best_original_ids[id][0])\
              + "*" + str(best_original_ids[id][1])

# version for test
def aggregate_tag_for_test(tag, stop_list):

    # parse, normalize and filter tag
    #cmd = 'echo '+ tag + '|' + NORMALIZER
    #p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    bag_of_words = filter_bag_of_words(tag.split(" "), stop_list)

    # find bag of words
    bag_of_words_ids = find_items_for_tag_for_test(bag_of_words)



    if len(bag_of_words_ids) == 0:
        #trying to cut kirillic letters and start again
        bag_of_words = filter_cyrillic(bag_of_words)
        if len(bag_of_words) != 0:
            bag_of_words_ids = find_items_for_tag_for_test(bag_of_words)


    #create set of answres

    answers = set()

    if len(bag_of_words_ids) != 0:
        for id in bag_of_words_ids.keys():
            answers.add(tag + "*" + str(IDBAG_BAG.get(id)).lower() +"*" + '%.2f' % (bag_of_words_ids[id][0])\
                        + "*" + '%.2f' % (bag_of_words_ids[id][1]) + "*" + str(int(id) % 3))
    return answers

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
    number_of_one_symbol_words = check_for_one_symbol_words(bag_of_words)
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
