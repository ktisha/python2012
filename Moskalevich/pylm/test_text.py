__author__ = 'Pavel Moskalevich'

import unittest
from text import Normalizer

class TestText(unittest.TestCase):
#    def setUp(self):
#        pass

    def test_norm1(self):
    #        tc = unittest.TestCase()
        text = Normalizer.normalize("test\\data\\hobbit.txt")
        self.assertEqual('<s> in a hole in the ground there lived a hobbit </s> <s> not a nasty <punc> dirty <punc> wet hole <punc> filled with the ends of worms and an oozy smell <punc> nor yet a dry <punc> bare <punc> sandy hole with nothing in it to sit down on or to eat <punc> it was a hobbit <punc> hole <punc> and that means comfort </s>',\
        text)

if __name__ == '__main__':
    unittest.main()
