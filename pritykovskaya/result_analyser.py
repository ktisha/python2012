from config import STOP_LIST_FILE
from normalizer import normalize_tag
from redises import connect_id_to_item, connect_bag_id_to_bag
from searcher.PlainSearcher import PlainSearcher
from utils import read_stop_list, filter_bag_of_words, filter_cyrillic

ID_TO_ITEM_REDIS = connect_id_to_item()
IDBAG_BAG = connect_bag_id_to_bag()

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

def return_back_to_original_ids_filter_categories(dict_ids_passed_threshold):
    my_dict = {}
    for key in dict_ids_passed_threshold.keys():
        if int(key)/3 + 1 not in my_dict.keys():
            my_dict[int(key)/3 + 1] = [0, 0, 0]
        my_dict[int(key)/3 + 1][int(key) % 3] = dict_ids_passed_threshold[key][0]+dict_ids_passed_threshold[key][1]

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

def intersected_only_with_cat(triplet):
    if triplet[0] == 0 and triplet[1] == 0:
        return True
    else:
        return False

PLAIN_SEARCHER = PlainSearcher()

def aggregate_tag(tag):
    stop_list = read_stop_list(STOP_LIST_FILE)

    # parse, normalize and filter tag
    # normalize
    bag_of_words = filter_bag_of_words(normalize_tag(tag).replace("\n", "").split("+"), stop_list)

    # link tag and items
    best_original_ids = return_back_to_original_ids_filter_categories(PLAIN_SEARCHER.find_bag_of_words_for_tag(bag_of_words))
    #best_original_ids = return_back_to_original_ids(bag_ids_passed_threshold)

    print (best_original_ids)

    id_item_redis = ID_TO_ITEM_REDIS

    if len(best_original_ids) == 0:
        #trying to cut cyrillic letters and start again
        bag_of_words = filter_cyrillic(bag_of_words)
        best_original_ids = return_back_to_original_ids_filter_categories(PLAIN_SEARCHER.find_bag_of_words_for_tag(bag_of_words))
        print (best_original_ids)

    for id in best_original_ids.keys():
        print tag + "*" + id_item_redis.get(id) +"*" + str(id) + "*" + str(best_original_ids[id][0])\
              + "*" + str(best_original_ids[id][1])

# version for test
def aggregate_tag_for_test(tag, stop_list):

    # parse, normalize and filter tag
#    tag = normalize_tag(tag)
    bag_of_words = filter_bag_of_words(tag.split(" "), stop_list)

    # find bag of words
    bag_of_words_ids = PLAIN_SEARCHER.find_bag_of_words_for_tag(bag_of_words)

    if len(bag_of_words_ids) == 0:
        #trying to cut kirillic letters and start again
        bag_of_words = filter_cyrillic(bag_of_words)
        if len(bag_of_words) != 0:
            bag_of_words_ids = PLAIN_SEARCHER.find_bag_of_words_for_tag(bag_of_words)

    #create set of answres

    answers = set()

    if len(bag_of_words_ids) != 0:
        for id in bag_of_words_ids.keys():
            answers.add(tag + "*" + str(IDBAG_BAG.get(id)).lower() +"*" + '%.2f' % (bag_of_words_ids[id][0])\
                        + "*" + '%.2f' % (bag_of_words_ids[id][1]) + "*" + str(int(id) % 3))
    return answers
