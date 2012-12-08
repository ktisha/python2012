__author__ = 'Pavel Moskalevich'

import unittest
from text import Normalizer, NgramMaker

class TestText(unittest.TestCase):
    def setUp(self):
        self.text = Normalizer.normalize("test\\data\\hobbit.txt")

    def test_norm1(self):
    #        tc = unittest.TestCase()
        self.assertEqual('<s> in a hole in the ground there lived a hobbit </s> <s> not a nasty <punc> dirty <punc> wet hole <punc> filled with the ends of worms and an oozy smell <punc> nor yet a dry <punc> bare <punc> sandy hole with nothing in it to sit down on or to eat <punc> it was a hobbit <punc> hole <punc> and that means comfort </s>',\
        self.text)

    def test_ngrams(self):
        maker = NgramMaker(3)
        maker.parse(self.text)
        for ng in maker:
            print ng, " :  ", maker.at(ng)

if __name__ == '__main__':
    unittest.main()
