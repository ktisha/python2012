__author__ = 'Pavel Moskalevich'

class Trie:
    ''' This class represents a trie data structure.
    Every node contains a word, absolute count of corresponding n-gram
    and probability along with back off weight (bow).
    '''

    class TrieNode:
        def __init__(self, count = 0, prob = 0, bow = 0):
            self.children = {}
            self.count    = count
            self.prob     = prob
            self.bow      = bow

        def add_child(self, word, count = 0, prob = 0, bow = 0):
            self.children[word] = Trie.TrieNode(count=count, prob=prob, bow=bow)

        def find_child(self, word):
            if self.children.has_key(word):
                return self.children[word]
            return None

    def __init__(self):
        self.root = Trie.TrieNode()

    def set_ngram(self, words, count = 0, prob = 0, bow = 0):
        ''' Add or modify n-gram. '''
        iter = self.root

        for w in words:
            if iter.find_child(w) == None:
                iter.add_child(w)
            iter = iter.children[w]

        iter.count = count
        iter.prob  = prob
        iter.bow   = bow

    def get_ngram(self, words):
        ''' Get n-gram (to read count, prob, bow). '''
        iter = self.root

        for w in words:
            if iter.find_child(w) == None:
                return None
            iter = iter.children[w]

        return iter
