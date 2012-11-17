# -*- coding:utf-8 -*-

__author__ = 'viteck.dudin'
__mail__ = 'viteck.dudin@yandex.ru'

file_handlers = {}

def main():
    """
    This script parses one big dictionary into several dictionaries,
    each with same word length
    """
    main_dict_filename = 'main_dict_utf8.txt'
    file_main = open(main_dict_filename, 'r')

    word_cnt = 0
    cur_cnt = 0
    for line in file_main:
        if cur_cnt == 10000:
            word_cnt += cur_cnt
            cur_cnt = 0
            print "Processed " + str(word_cnt) + " words"
        add_word(line)
        cur_cnt += 1
    word_cnt += cur_cnt
    print "Totally processed " + str(word_cnt) + " words"

    file_main.close()
    close_all_files()

def add_word(text):
    if text[-1] == '\n':
        text = text[:-1]

    length = len(text.decode('utf-8'))
    if length > 0:
        f = get_file(length)
        print >>f, text

def get_file(word_len):
    if word_len in file_handlers:
        return file_handlers[word_len]
    else:
        filename = "dict_" + str(word_len) + ".txt"
        open_file(filename, word_len)
        return file_handlers[word_len]

def open_file(filename, word_len):
    file_handler = open(filename, 'w')
    if word_len in file_handlers:
        print "AHTUNG!!! Incorrect work with file handlers: attempt to create repeated handler"
        exit()
    file_handlers[word_len] = file_handler
    return file_handler

def close_all_files():
    for fh in file_handlers.values():
        fh.close()

if __name__ == "__main__":
    main()