__author__ = 'Pavel Moskalevich'

class Ngram:
    def __init__(self, count = 0, prob = 0):
        self.count = count
        self.prob  = prob

    def set_count(self, count):
        self.count = count

    def set_prob(self, prob):
        self.prob = prob


class NgramStorage:
    def __init__(self, max_order):
        self.n_grams    = {}
        self.max_order_ = max_order

    def __iter__(self):
        return self.n_grams.__iter__()

    def set_n_gram(self, words_tuple, ngram):
        if len(words_tuple) > self.max_order_:
            return

        if not self.n_grams.has_key(len(words_tuple)):
            self.n_grams[len(words_tuple)] = {}
        self.n_grams[len(words_tuple)][words_tuple] = ngram

    def get_n_gram(self, words_tuple):
        if not self.n_grams.has_key(len(words_tuple)) or not self.n_grams[len(words_tuple)].has_key(words_tuple):
            return None
        return self.n_grams[len(words_tuple)][words_tuple]

    def get_n_grams(self, order):
        if not self.n_grams.has_key(order):
            return []
        return filter(lambda x: len(x) == order, self.n_grams[order].keys())

    def max_order(self):
        return self.max_order_

    def total_n_grams(self, order = 0):
        ''' Returns total number of n-grams of order (sum of all counts).
        If order is zero, than summarizes across all orders.
        '''
        if order == 0:
            summa = 0
            for ng_ord in self.n_grams.keys():
                summa = summa + reduce(lambda cum, x: cum + self.n_grams[ng_ord][x].count, self.n_grams[ng_ord].keys(), 0)
            return summa
        else:
            if self.n_grams.has_key(order):
                return reduce(lambda cum, x: cum + self.n_grams[order][x].count, self.n_grams[order].keys(), 0)
            else:
                return 0

    def distinct_n_grams(self, order = 0):
        ''' Returns number of distinct n-grams of order.
        If order is zero, than counts across all orders.
        '''
        if order == 0:
            return reduce(lambda cum, x: cum + len(self.n_grams[x]), self.n_grams.keys(), 0)
        else:
            if self.n_grams.has_key(order):
                return len(self.n_grams[order])
            else:
                return 0
