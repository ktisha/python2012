# coding=utf-8
import re
from nltk.tokenize import wordpunct_tokenize

from config import STOP_LIST_FILE

def read_stop_list():
    input = open(STOP_LIST_FILE, "r")
    stop_list = set()

    for line in input:
        stop_list.add(line.lower().rstrip())
    input.close()

    return stop_list

def parse_line(line):
    return map(lambda x: x.lower(), wordpunct_tokenize(line))
def filter_bag_of_words(bag, stop_list):
    return set(filter(lambda x: x not in stop_list, bag))
def normalize_bag_of_words(bag, norm_index):
    new_bag = set()
    for word in bag:
        if norm_index.exists(word):
            norm_word = norm_index.get(word)
            if norm_word != "":
                new_bag.add(norm_word)
        else: pass
    return new_bag
def parse_data(data, stop_list):
    word_bag = set()
    for rec in data:
        for text in rec[1:]:
            #print text
            word_bag |= set(parse_line(text)) #filter_bag_of_words(parse_line(text), stop_list)
    return word_bag
def contain_only_ascii(word):
    if re.match("^[A-Za-z0-9]+$", word):
        return word
def filter_cyrillic(bag_of_words):
    return filter(lambda x: contain_only_ascii(x), bag_of_words)
def check_if_one_symbol_word(word):
    if len(word) == 1:
        return 1
    else:
        return 0