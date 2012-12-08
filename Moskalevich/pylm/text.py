__author__ = 'Pavel Moskalevich'

import re
from ngram import Ngram, NgramStorage

class Normalizer:
    ''' This class normalizes text from file.
    '''

    @staticmethod
    def normalize(file):
        lines = open(file).readlines()
        text = ' '.join(map(lambda x: x.strip(), lines))
        text = Normalizer._replace_punc_(text)
        text = Normalizer._change_case_(text)
        text = Normalizer._rm_whitespace_(text)
        return text

    @staticmethod
    def _replace_punc_(text):
        text = re.sub('[\,:;\-\(\)\[\]\"\{\}<>=\+\*_\\/]+', ' <punc> ', text)
        text = re.sub('^', '<s> ', text)
        endOfSent = '[\.!?]+'
        text = re.sub(endOfSent + '$', ' </s>', text)
        text = re.sub(endOfSent, ' </s> <s> ', text)
        return text

    @staticmethod
    def _change_case_(text):
        return text.lower()

    @staticmethod
    def _rm_whitespace_(text):
        text = text.strip()
        return re.sub('\s+', ' ', text)


#text = Normalizer.normalize('test\\data\\hobbit.txt')
#print text

class NgramMaker:
    ''' This class holds ngrams, made from text.
    '''

    def __init__(self, max_order):
        self.max_order = max_order
        self.storage_  = NgramStorage()

    def parse(self, text):
        tokens = re.split('\s+', text)
        for wnum in xrange(0, len(tokens)):
            for ng_ord in xrange(1, self.max_order + 1):
                if wnum + ng_ord < len(tokens):
                    words_tuple = tuple(tokens[wnum : wnum + ng_ord])
                    ngram = self.storage_.get_n_gram(words_tuple)
                    if  ngram == None:
                        ngram = Ngram(1)
                    else:
                        ngram.count = ngram.count + 1
                    self.storage_.set_n_gram(words_tuple, ngram)

    def __iter__(self):
        return self.storage_.__iter__()

    def storage(self):
        return self.storage_

    def at(self, words_tuple):
        ngram = self.storage_.get_n_gram(words_tuple)
        if  ngram == None:
            ngram = Ngram(0)
        return ngram