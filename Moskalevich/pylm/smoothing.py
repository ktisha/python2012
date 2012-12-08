__author__ = 'happy'

from ngram import Ngram,NgramStorage
from math import log10, pow

class GoodTuring:
    def __init__(self, ng_storage, gtNmin):
        self.ng_storage = ng_storage
        self.gtNmin     = gtNmin
        # interpolation parameters
        self.coc        = {}
        self.a          = 0
        self.b          = 0

        for ng_ord in xrange(1, ng_storage.max_order() + 1):
            self._probs_order_(ng_ord)

    def storage(self):
        return self.ng_storage

    def _probs_order_(self, order):
        total_count = self.ng_storage.total_n_grams(order)
        ngs         = self.ng_storage.get_n_grams(order)

        self._interpolate_(order)   # compute smoothing parameters for current order

        for ng in ngs:
            ngram = self.ng_storage.get_n_gram(ng)
            if ngram.count < self.gtNmin[order - 1]:
                # use smoothing when count is to low (we can't rely on it)
                # this is where Good-Turing smoothing works
                A = float(self.gtNmin[order - 1] + 1) * self._get_interpolated_(self.gtNmin[order - 1] + 1)\
                    / self._get_interpolated_(1)
                CC = float(ngram.count + 1) * self._get_interpolated_(ngram.count + 1)\
                     / self._get_interpolated_(ngram.count)
                smooth = float(CC / ngram.count - A) / (1 - A)
            else:
                smooth = 1
            # don't want to compute log10 of too little numbers
            if smooth < 0.00000001:
                smooth = 0.00000001

            if order == 1:
                ngram.prob = log10(ngram.count) - log10(total_count) + log10(smooth)
            else:
                ngram.prob = log10(ngram.count) - log10(self.ng_storage.get_n_gram(ng[0:-1]).count) + log10(smooth)
            self.ng_storage.set_n_gram(ng, ngram)


    def _counts_of_counts_(self, order):    # compute counts of counts for certain order
        self.coc = {}
        ngs = self.ng_storage.get_n_grams(order)
        for ng in ngs:
            count = self.ng_storage.get_n_gram(ng).count
            if self.coc.has_key(count):
                self.coc[count] = self.coc[count] + 1
            else:
                self.coc[count] = 1

    def _interpolate_(self, order): # compute interpolation parameters for missing counts of counts
        self._counts_of_counts_(order)
        sorted_coc = sorted(self.coc.keys())

        N          = len(sorted_coc)
        log_counts = map(lambda c: log10(c), sorted_coc)

        xMean  = 0
        yMean  = 0
        xyMean = 0
        xSqMean = 0
        for i in xrange(0, N):
            xMean   = xMean + sorted_coc[i]
            yMean   = yMean + log_counts[i]
            xyMean  = xyMean + sorted_coc[i] * log_counts[i]
            xSqMean = xSqMean + sorted_coc[i] * sorted_coc[i]

        xMean   = xMean / N
        yMean   = yMean / N;
        xyMean  = xyMean / N
        xSqMean = xSqMean / N

        # linear interpolation parameters
        self.a = (xSqMean * yMean - xMean * xyMean) / (xSqMean - xMean * xMean)
        self.b = (xyMean - xMean * yMean) / (xSqMean - xMean * xMean)

    def _get_interpolated_(self, count):
        if self.coc.has_key(count):
            return self.coc[count]
        else:
            return pow(10, (self.a + self.b * count))
