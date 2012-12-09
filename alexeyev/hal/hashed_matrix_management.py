#!/usr/bin/python
#-*- coding: utf-8 -*-
from _sortedlist import sortedset

__author__ = 'Anton M Alexeyev'

class HashedWordMatrix:

    def __init__(self):
        self.dict = {}

    def get_tokens(self):
        return self.dict.keys()

    def add(self, first, second, value):
        if self.dict.has_key(first):
            if self.dict[first][1].has_key(second):
                self.dict[first][1][second] += value
            else:
                self.dict[first][1][second]  = value
        else:
            self.dict[first] = [{}, {second : value}]

        if self.dict.has_key(second):
            if self.dict[second][0].has_key(first):
                self.dict[second][0][first] += value
            else:
                self.dict[second][0][first]  = value
        else:
            self.dict[second] = [{first : value}, {}]

    def get(self, target, first, second):
        """Getting the value of the cell in the matrix; target -- row"""
        if first == target:
            if self.dict.has_key(first):
                if self.dict[first][1].has_key(second):
                    return self.dict[first][1][second]
                else:
                    return 0
            return 0
        else:
            if self.dict.has_key(second):
                if self.dict[second][0].has_key(first):
                    return self.dict[second][0][first]
                else:
                    return 0
            return 0

    def normalize(self):
        """Normalizing lengths of rows"""
        for key in self.dict.keys():
            collector = 0.0
            for help_key in self.dict.keys():
                collector += self.get(key, help_key, key) ** 2
                collector += self.get(key, key, help_key) ** 2
            for help_key in self.dict.keys():
                if self.dict.has_key(key) and self.dict[key][0].has_key(help_key):
                    self.dict[key][0][help_key] /= collector ** 0.5
                if self.dict.has_key(key) and self.dict[key][1].has_key(help_key):
                    self.dict[key][1][help_key] /= collector ** 0.5

    def dist_cols_euclidean(self, col0, col1):
        """Measures distance between 2 columns: Euclidean distance"""
        collector = 0
        for key in self.get_tokens():
            collector += (self.get(col0, col0, key) - self.get(col1, col1, key)) ** 2
            collector += (self.get(col0, key, col0) - self.get(col1, key, col1)) ** 2
        return collector ** 0.5

    def dist_cols_manhattan(self, col0, col1):
        """Measures distance between 2 columns: Manhattan distance"""
        collector = 0
        for key in self.get_tokens():
            collector += abs(self.get(col0, col0, key) - self.get(col1, col1, key))
            collector += abs(self.get(col0, key, col0) - self.get(col1, key, col1))
        return collector

    def dist_cols_inverted_cosine(self, col0, col1):
        """Measures distance between 2 columns: Cosine similarity"""
        length0 = 0.0
        length1 = 0.0
        collector = 0.0

        for key in self.get_tokens():
            k0 = self.get(col0, col0, key)
            kk0 = self.get(col0, key, col0)
            k1 = self.get(col1, col1, key)
            kk1 = self.get(col1, key, col1)
            collector += k0 * k1
            collector += kk0 * kk1
            #length0 += k0 ** 2 + kk0 ** 2
            #length1 += k1 ** 2 + kk1 ** 2
        #length0 **= 0.5
        #length1 **= 0.5
#        return length0 * length1 / collector  #if collector > 0 else 0.000000000001
        return 1 / collector

    def kn_columns(self, target_column, k, dist_func):
        """Gets k nearest columns to target_column by distance function provided by dist_func"""
        n = len(self.get_tokens())
        coolset = sortedset()
        for word in self.get_tokens():
            if word <> "*":
                coolset.add((dist_func(target_column, word), word))
        array = list(coolset[1 : k + 1])
        return array

    def kn_cooccurences(self, target_column, k):
        """Gets k top columns having max cooccurence with target_column"""
        coolset = sortedset()
        for word in self.get_tokens():
            if word <> "*":
                coolset.add((self.get(target_column, target_column, word), word))
        array = list(coolset[len(coolset) - k : len(coolset)])
        array.reverse()
        return array
