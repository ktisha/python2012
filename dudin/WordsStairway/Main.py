__author__ = 'viteck.dudin'
__mail__ = 'viteck.dudin@yandex.ru'

import sys
import Dictionary


def main(start_word, end_word, dictionary_filename):
    while start_word[-1] == '\n':
        start_word = start_word[:-1]
    while end_word[-1] == '\n':
        end_word = end_word[:-1]
    while dictionary_filename[-1] == '\n':
        dictionary_filename = dictionary_filename[:-1]

    words_dict = Dictionary.Dictionary(start_word, end_word, dictionary_filename)
    words_stairway = words_dict.create_stairway()
    for word in words_stairway:
        print word


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Wrong number of parameters"
        print "Usage: start_word end_word dictionary_filename"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])