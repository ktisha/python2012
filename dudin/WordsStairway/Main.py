# -*- coding:utf-8 -*-

__author__ = 'viteck.dudin'
__mail__ = 'viteck.dudin@yandex.ru'

import sys
import Dictionary


def main(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        start_word = lines[0].decode('utf-8')
        end_word = lines[1].decode('utf-8')
    if start_word[-1] == '\n':
        start_word = start_word[:-1]
    if end_word[-1] == '\n':
        end_word = end_word[:-1]

    dict_filename = 'dictionaries/dict_' + str(len(start_word)) + '.txt'
    dict_filename = dict_filename.decode('utf-8')

    words_dict = Dictionary.Dictionary(start_word, end_word, dict_filename)
    print "Dictionary is loaded"

    words_stairway = words_dict.create_stairway()
    for word in words_stairway:
        print word

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Wrong number of parameters"
        print "Usage: target_words_filename"
    else:
        main(sys.argv[1])