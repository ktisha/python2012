__author__ = 'Pavel Moskalevich'

import unittest
from ngram import Trie

class TestText(unittest.TestCase):
#    def setUp(self):
#        pass

    def test_simple(self):
    #        tc = unittest.TestCase()
        words1 = ["hello", "<punc>", "world"]
        words2 = ["hello", "<punc>", "underworld"]
        words3 = ["hello", "<punc>", "John"]
        words4 = ["goodbye", "<punc>", "John"]
        trie = Trie()
        trie.set_ngram(words1[0], 12, 0.1)
        trie.set_ngram(words1[0:1], 10, 0.08)
        trie.set_ngram(words1, 4, 0.02)
        trie.set_ngram(words2, 4, 0.02)
        trie.set_ngram(words3, 2, 0.01)
        trie.set_ngram(words4, 8, 0.05)

        epsilon = 0.00001

        self.assertEqual(8, trie.get_ngram(words4).count)
        self.assertLess(abs(0.05 - trie.get_ngram(words4).prob), epsilon)
        self.assertEqual(4, trie.get_ngram(words1).count)
        self.assertLess(abs(0.02 - trie.get_ngram(words1).prob), epsilon)
        self.assertEqual(0, trie.get_ngram(words4[0:1]).count)
        self.assertLess(trie.get_ngram(words4[0:1]).prob, epsilon)

if __name__ == '__main__':
    unittest.main()
