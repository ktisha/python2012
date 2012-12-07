__author__ = 'Anton M Alexeyev'

import blist
from blist import sortedset

class WordMatrix:
    """
    Sparse matrix presented as a dictionary "(token0, token1)->value".
    Implementation may change later.
    """
    def __init__(self):
        self.matrix = {("", "") : 0}
        self.token_set = []

    def add(self, first_token, second_token, value):
        """Adds given value to the given cell"""
        if not self.matrix.has_key((first_token, second_token)):
            self.matrix[(first_token, second_token)] = 0
        self.matrix[(first_token, second_token)] += value
        if not first_token in self.token_set:
            self.token_set += [first_token]
        if not second_token in self.token_set:
            self.token_set += [second_token]

    def get(self, first_token, second_token):
        """Gets cell with given coords"""
        if not self.matrix.has_key((first_token, second_token)):
            return 0
        return self.matrix[(first_token, second_token)]

    def get_tokens(self):
        """Gets all the tokens in stock"""
        return self.token_set

    def dist_cols_euclidean(self, col0, col1):
        """Measures distance between 2 columns: Euclidean distance"""
        collector = 0
        for key in self.token_set:
            collector += (self.get(key, col0) - self.get(key, col1)) ** 2
            collector += (self.get(col0, key) - self.get(col1, key)) ** 2
        return collector**0.5

    def dist_cols_inverted_cosine(self, col0, col1):
        """Measures distance between 2 columns: Cosine similarity"""
        length0 = 0.0
        length1 = 0.0
        collector = 0.0

        for key in self.token_set:
            k0 = self.get(key, col0)
            k1 = self.get(key, col1)
            collector += k0 * k1
            collector += self.get(col0, key) * self.get(col1, key)
            length0 +=  2 * (k0**2)
            length1 +=  2 * (k1**2)
        length0 **= 0.5
        length1 **= 0.5
        return (0.0 + length0 * length1) / (collector + 0.0)

    def kn_columns(self, target_column, k, dist_func):
        """Gets k nearest columns to target_column by distance function provided by dist_func"""
        n = len(self.token_set)
        coolset = sortedset()
        for word in self.token_set:
            if word <> "*":
                coolset.add((dist_func(target_column, word), word))
        array = list(coolset[1 : k + 1])
        return array

    def kn_cooccurences(self, target_column, k):
        """Gets k top columns having max cooccurence with target_column"""
        n = len(self.token_set)
        coolset = sortedset()
        for word in self.token_set:
            if word <> "*":
                coolset.add((self.get(target_column, word), word))
        array = list(coolset[len(coolset) - k : len(coolset)])
        array.reverse()
        return array