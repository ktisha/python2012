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
        if not isinstance(text, str):
            raise Exception("Input word is not a string (input: " + str(text) + ")")
        self.text = (str(text)).upper()


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
        self.words_buckets[self.__calc_words_dif(self.start_word, self.end_word)] = [self.start_word]
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
                # Make checks for text
                if text[-1] == '\n':
                    text = text[:-1]
                # Save only that words, which have the same length with start_word and end_word
                if len(text) != self.word_length and len(text) > 0:
                    print "Word [" + text + "] not added into dictionary (reason: incorrect length)"
                    continue
                # All ok, create new Word
                word = Word(text)
                word.global_index = self.dictionary_size
                self.dictionary_size += 1
                self.__add_word_into_dictionary(word)

    def __add_word_into_dictionary(self, word):
        bucket = self.__calc_words_dif(word, self.end_word)
        Word(word).bucket_number = bucket

        if bucket not in self.words_buckets:
            self.words_buckets[bucket] = []

        all_ok = True
        # Check unique, if necessary
        if self.check_unique_words_in_dictionary:
            all_ok = self.__check_unique(word, self.words_buckets[bucket])
        if all_ok:
            self.words_buckets[bucket].append(word)

    def __check_unique(self, word, word_list):
        # TODO: Need to be released
        raise Exception("Unsupported operation")

    def __calc_words_dif(self, word1, word2):
        length = len(word1)
        dif = 0
        for x in xrange(length):
            if word1[x] != word2[x]:
                dif += 1
        return dif

    def create_stairway(self):
        # create stairway, using analog of bfs in graphs
        self.words_queue = []
        self.words_queue.append(self.start_word)

        # TODO: need to be released
        raise Exception("Unsupported operation")


