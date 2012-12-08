from _sortedlist import sortedset

__author__ = 'Anton M Alexeyev'

class HashedWordMatrix:

    def __init__(self):
        self.dict = {}

    def add(self, first, second, value):
        if dict.has_key(first):
            if dict[first][1].has_key(second):
                dict[first][1][second] += value
            else:
                dict[first][1][second]  = value
        else:
            dict[first] = [{}, {second : value}]

        if dict.has_key(second):
            if dict[second][0].has_key(first):
                dict[second][0][first] += value
            else:
                dict[second][0][first]  = value
        else:
            dict[second] = [{first : value}, {}]

    def get(self, first, second):
        if dict.has_key(first):
            if dict[first][1].has_key(second):
                return dict[first][1][second]
            else:
                return 0
        return 0

    def normalize(self):
        for key in dict.keys():
            collector = 0.0
            # todo: make valid
            for help_key in dict.keys():
                collector += dict[key][0][help_key]
                collector += dict[key][1][help_key]
            for help_key in dict.keys():
                dict[key][0][help_key] /= (collector)
                dict[key][1][help_key] /= (collector)

    def dist_cols_euclidean(self, col0, col1):
        """Measures distance between 2 columns: Euclidean distance"""
        collector = 0
        for key in self.token_set:
            collector += (self.get(key, col0) - self.get(key, col1)) ** 2
            collector += (self.get(col0, key) - self.get(col1, key)) ** 2
        return collector ** 0.5

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
        print length1
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
