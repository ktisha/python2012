__author__ = 'Pavel Moskalevich'

import re

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