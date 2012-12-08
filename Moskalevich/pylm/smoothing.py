__author__ = 'happy'

from ngram import Ngram,NgramStorage

class GoodTuring:
    def __init__(self, ng_storage):
        self.ng_storage = ng_storage
        for ng_ord in xrange(1, ng_storage.max_order() + 1):
            self._probs_order_(ng_ord)

    def storage(self):
        return self.ng_storage

    def _probs_order_(self, order):
        total_count    = self.ng_storage.total_n_grams(order)
        ngs            = self.ng_storage.get_n_grams(order)

        for ng in ngs:
            ngram = self.ng_storage.get_n_gram(ng)
            if order == 1:
                ngram.prob = float(ngram.count) / total_count
            else:
                ngram.prob = float(ngram.count) / (self.ng_storage.get_n_gram(ng[0:-1]).count)
            self.ng_storage.set_n_gram(ng, ngram)



