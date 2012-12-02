__author__ = 'Pavel Moskalevich'

import unittest
from ngram import Ngram, NgramStorage

class TestText(unittest.TestCase):
#    def setUp(self):
#        pass

    def test_simple(self):
    #        tc = unittest.TestCase()
        words1 = ("hello", "<punc>", "world")
        words2 = ("hello", "<punc>", "underworld")
        words3 = ("hello", "<punc>", "John")
        words4 = ("goodbye", "<punc>", "John")
        ng = NgramStorage()
        ng.set_n_gram(words1[0], Ngram(12, 0.1))
        ng.set_n_gram(words1[0:1], Ngram(10, 0.08))
        ng.set_n_gram(words1, Ngram(4, 0.02))
        ng.set_n_gram(words2, Ngram(4, 0.02))
        ng.set_n_gram(words3, Ngram(2, 0.01))
        ng.set_n_gram(words4, Ngram(8, 0.05))

        epsilon = 0.00001

        self.assertEqual(8, ng.get_n_gram(words4).count)
        self.assertLess(abs(0.05 - ng.get_n_gram(words4).prob), epsilon)
        self.assertEqual(4, ng.get_n_gram(words1).count)
        self.assertLess(abs(0.02 - ng.get_n_gram(words1).prob), epsilon)
        self.assertIsNone(ng.get_n_gram(words4[0]))
        self.assertIsNone(ng.get_n_gram(words4[0:1]))

if __name__ == '__main__':
    unittest.main()
