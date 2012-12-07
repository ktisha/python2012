# -*- coding:utf-8 -*-

__author__ = 'viteck.dudin'
__mail__ = 'viteck.dudin@yandex.ru'

import sys
import Dictionary


def main(filename):
    with open(filename, 'r') as f:
        lines = ''.join(f.readlines()).split()
        start_word = lines[0].decode('utf-8')
        end_word = lines[1].decode('utf-8')

    dict_filename = 'dictionaries/dict_' + str(len(start_word)) + '.txt'
    dict_filename = dict_filename.decode('utf-8')

    try:
        words_dict = Dictionary.Dictionary(start_word, end_word, dict_filename)
        print "Dictionary is loaded"
        words_stairway = words_dict.create_stairway()
        for word in words_stairway:
            print word
        print "Length of created stairway (number of changes): " + str(len(words_stairway) - 1)
    except Dictionary.MyException as e:
        print 'Error! ' + e.value
        exit(-1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: target_words_filename"
        print "For more information, look README file"
    else:
        main(sys.argv[1])