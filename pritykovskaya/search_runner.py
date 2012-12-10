# coding=utf-8

from normalizer import normalize_tag
from redises import connect_id_to_item, connect_bag_id_to_bag
from utils import filter_bag_of_words, filter_cyrillic
from common import STOP_LIST

ID_TO_ITEM_REDIS = connect_id_to_item()
IDBAG_BAG = connect_bag_id_to_bag()

def convert_tag_to_word_bag(tag, is_tag_normalized):
    if is_tag_normalized:
        tag_lego = tag.lower().split(" ")
    else:
        tag_lego = normalize_tag(tag)
    return filter_bag_of_words(tag_lego, STOP_LIST)

def run_searcher(searcher, tag, is_tag_normalized):
    bag_of_words = convert_tag_to_word_bag(tag, is_tag_normalized)
    bag_of_words_ids = searcher.find_bag_of_words_for_tag(bag_of_words)

    if len(bag_of_words_ids) == 0:
        #trying to cut cyrillic letters and start again
        bag_of_words = filter_cyrillic(bag_of_words)
        if len(bag_of_words) != 0:
            bag_of_words_ids = searcher.find_bag_of_words_for_tag(bag_of_words)

    return bag_of_words_ids

def return_back_to_original_ids_filter_categories(dict_ids_passed_threshold):
    my_dict = {}
    my_dict_bags = {}

    for key in dict_ids_passed_threshold.keys():
        if int(key)/3 + 1 not in my_dict.keys():
            my_dict[int(key)/3 + 1] = [0, 0, 0]
            my_dict_bags[int(key)/3 + 1] = ["", "", ""]
        my_dict[int(key)/3 + 1][int(key) % 3] = dict_ids_passed_threshold[key][0] + dict_ids_passed_threshold[key][1]
        my_dict_bags[int(key)/3 + 1][int(key) % 3] = IDBAG_BAG.get(key)

    # should choose best sum and write stat with which bad ids tag has intersected
    # what I want to know is there cases when intersection with category or descr  made difference
    # it's obvious that if tags have same cat there can't be any difference

    win_competitor_without_cat = 0
    win_competitor_with_another_cat = 0
    win_competitor_without_descr = 0
    has_winner_cat = 0
    has_winner_descr = 0
    best_key = -1

    max = 0
    best_ids = {}
    best_bags = {}

    for key in my_dict:
        if sum(my_dict[key]) > max:
            # у предыдущего победителя не было категории, у текущего есть она и еще что-то
            if not has_winner_cat and (my_dict[key][2] > 0) and (my_dict[key][0] > 0 | my_dict[key][1] > 0):
                win_competitor_without_cat = 1

            # у предыдущего победителя была категория, но она не совпадает с текущей + у текущего победителя есть еще что-то
            if best_key > 0 and has_winner_cat and (my_dict[key][2] > 0) and \
               my_dict_bags[best_key][2] != my_dict_bags[key][2] and (my_dict[key][0] > 0 | my_dict[key][1] > 0):
                win_competitor_with_another_cat = 1

            # у предыдущего не было категории, у текущего есть оно и еще что-то
            if not has_winner_descr and (my_dict[key][1] > 0) and (my_dict[key][0] > 0 | my_dict[key][2] > 0):
                win_competitor_without_descr = 1
                
            max = sum(my_dict[key])
            best_ids.clear()
            best_key = key
            best_ids[key] = [max, my_dict[key][0], my_dict[key][1], my_dict[key][2]]
            best_bags[key] = [my_dict_bags[key][0], my_dict_bags[key][1], my_dict_bags[key][2]]
            has_winner_cat = my_dict[key][2] > 0
            has_winner_descr = my_dict[key][1] > 0
        else:
            if sum(my_dict[key]) == max:
                best_ids[key] = [max, my_dict[key][0], my_dict[key][1], my_dict[key][2]]
                best_bags[key] = [my_dict_bags[key][0], my_dict_bags[key][1], my_dict_bags[key][2]]
    return best_ids, best_bags, [win_competitor_without_cat, win_competitor_with_another_cat, win_competitor_without_descr]

def intersected_only_with_cat(triplet):
    if triplet[0] == 0 and triplet[1] == 0:
        return True
    else:
        return False

# return set of text results in my specific form
def aggregate_tag(searcher, tag, tag_is_normalized):
    bag_of_words_ids = run_searcher(searcher, tag, tag_is_normalized)
    best_original_ids, best_bags, competitors_info = return_back_to_original_ids_filter_categories(bag_of_words_ids)

    answers = set()
    for id in best_original_ids.keys():
        answers.add(tag + "*" + ID_TO_ITEM_REDIS.get(id) +"*" + str(id) + "*" + str(best_original_ids[id][0])\
              + "*" + str(int(best_original_ids[id][1] > 0)) + "*" + str(int(best_original_ids[id][2] > 0))\
              + "*" + str(int(best_original_ids[id][3] > 0)) + "*" + best_bags[id][0] \
              + "*" + best_bags[id][1] + "*" + best_bags[id][2] + "*" + str(competitors_info[0]) \
              + "*" + str(competitors_info[1]) + "*" + str(competitors_info[2]))
    return answers

# return set of text results in test (like Kristina) specific form
def aggregate_tag_for_test(searcher, tag, tag_is_normalized):
    bag_of_words_ids = run_searcher(searcher, tag, tag_is_normalized)

    answers = set()
    if len(bag_of_words_ids) != 0:
        for id in bag_of_words_ids.keys():
            answers.add(tag + "*" + str(IDBAG_BAG.get(id)).lower() +"*" + '%.2f' % (bag_of_words_ids[id][0])\
                        + "*" + '%.2f' % (bag_of_words_ids[id][1]) + "*" + str(int(id) % 3))
    return answers
