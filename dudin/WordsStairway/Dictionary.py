# -*- coding:utf-8 -*-

__author__ = 'viteck.dudin'
__mail__ = 'viteck.dudin@yandex.ru'


class Word:
    """
    Class describes any word from input dictionary
    """
    text = ""
    global_index = -1
    bucket_number = -1
    parent_index = -1

    def __init__(self, text):
        if isinstance(text, str):
            self.text = text.decode('utf-8')
        elif isinstance(text, unicode):
            self.text = text
        else:
            raise Exception("Input word is not a string (input: " + str(text) + ")")
        self.text = self.text.upper()


class Dictionary:
    check_unique_words_in_dictionary = True

    def __init__(self, start_word, end_word, dictionary_filename):
        self.start_word = Word(start_word)
        self.end_word = Word(end_word)
        if len(start_word) != len(end_word):
            raise Exception("Incorrect input: start_word (" + self.start_word.text +
                            ") and end_word (" + self.end_word.text + ") has different lengths")
        if len(start_word) == 0:
            raise Exception("Incorrect input: words should have non-zero lengths")
        self.word_length = len(start_word)

        # Add start_word into dictionary
        self.words_buckets = {}
        self.start_word.global_index = 0
        self.start_word.bucket_number = self.__calc_words_dif(self.start_word, self.end_word)
        self.start_word.parent_index = -2   # unique index. using it, we won't get parent for start_word
        self.words_buckets[self.start_word.bucket_number] = [self.start_word]
        # Add end_word into dictionary
        self.end_word.global_index = 1
        self.words_buckets[0] = [self.end_word]
        with open(dictionary_filename, "r") as fin:
            self.__read_input_dictionary(fin)

    def __read_input_dictionary(self, fin):
        # in bucket with key i there will be words, which differ from end_word with i symbols
        self.dictionary_size = 2

        for line in fin:
            for text in line.split():
                text = text.decode('utf-8')
                # Save only that words, which have the same length with start_word and end_word
                if len(text) != self.word_length and len(text) > 0:
                    print "Word [" + text + "] not added into dictionary (reason: incorrect length, "\
                          + str(len(text)) + " instead of " + str(self.word_length) + ")"
                    continue
                # All ok, create new Word
                word = Word(text)
                self.__add_word_into_dictionary(word)

    def __add_word_into_dictionary(self, word):
        bucket = self.__calc_words_dif(word, self.end_word)
        word.bucket_number = bucket

        if bucket not in self.words_buckets:
            self.words_buckets[bucket] = []

        all_ok = True
        # Check unique, if necessary
        if self.check_unique_words_in_dictionary:
            all_ok = self.__check_unique(word, self.words_buckets[bucket])
        if all_ok:
            word.global_index = self.dictionary_size
            self.dictionary_size += 1
            self.words_buckets[bucket].append(word)

    def __check_unique(self, word, word_list):
        for existing_word in word_list:
            if existing_word.text == word.text:
                return False
        return True

    def __calc_words_dif(self, word1, word2):
        text1 = word1.text
        text2 = word2.text

        length = len(text1)
        dif = 0
        for x in xrange(length):
            if text1[x] != text2[x]:
                dif += 1
        return dif

    def create_stairway(self):
        self.__create_stairway()
        print "Stairway is created"

        self.__restore_stairway()
        text_ls = []
        for word in self.stairway_ls:
            text_ls.append(word.text)
        return text_ls

    def __create_stairway(self):
        # create stairway, using analog of bfs in graphs
        self.words_queue = []
        self.words_queue.append(self.start_word)
        self.words_queue_cur_index = 0
        while self.end_word.parent_index == -1 and self.words_queue_cur_index < len(self.words_queue):
            self.__make_next_stairway_step()

    def __make_next_stairway_step(self):
        #print "In __make_next_stairway_step"
        cur_word = self.words_queue[self.words_queue_cur_index]
        self.words_queue_cur_index += 1

        # we need to check only words from buckets, which differ from current bucket
        # by no more than 1
        cur_bucket = cur_word.bucket_number
        # 0. check, that we in 1 step to end_word
        if cur_bucket == 1:
            self.end_word.parent_index = cur_word.global_index
            return
        # 1. check bucket with smaller number
        self.__process_bucket_in_stairway_step(cur_word, cur_bucket - 1)
        # 2. check bucket with same number. don't need to check bucket existence
        self.__process_bucket_in_stairway_step(cur_word, cur_bucket)
        # 3. check bucket with higher number, if it exists
        self.__process_bucket_in_stairway_step(cur_word, cur_bucket + 1)

    def __process_bucket_in_stairway_step(self, cur_word, bucket_index):
        if bucket_index in self.words_buckets.keys():
            for next_word in self.words_buckets[bucket_index]:
                if next_word.parent_index == -1 and self.__differ_by_one(cur_word, next_word):
                    next_word.parent_index = cur_word.global_index
                    self.words_queue.append(next_word)

    def __differ_by_one(self, word1, word2):
        # TODO: improvement check should be done there
        if word1 is word2:
            return False
        dif = self.__calc_words_dif(word1, word2)
        return dif == 1

    def __restore_stairway(self):
        if self.end_word.parent_index == -1:
            print "Impossible to build stairway from " + self.start_word.text + " to " + self.end_word.text
            exit()

        # collect all Words in one list, so it is easier to restore stairway
        all_words = []
        for word_list in self.words_buckets.values():
            all_words += word_list
        all_words.sort(key=lambda x : x.global_index)

        # restore stairway, saving it into self.stairway_ls
        self.stairway_ls = [self.end_word]
        cur_parent_index = self.end_word.parent_index
        while cur_parent_index != -2:
            prev_word = all_words[cur_parent_index]
            cur_parent_index = prev_word.parent_index
            self.stairway_ls.append(prev_word)
        self.stairway_ls = self.stairway_ls[::-1]

    def __print_dictionary(self):
        for key in self.words_buckets.keys():
            ls = self.words_buckets[key]
            print "Key is " + str(key)
            for word in ls:
                print word.text
