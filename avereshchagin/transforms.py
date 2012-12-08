import math
import numpy as np

__author__ = 'Aleksandr Vereshchagin'

class AbstractTransform:

    def transform(self, src):
        pass

    def transformSequence(self, srcSeq):
        return map(lambda x: self.transform(x), srcSeq)

    def inverseTransform(self, src):
        pass

    def inverseTransformSequence(self, srcSeq):
        return map(lambda x: self.inverseTransform(x), srcSeq)


class WalshHadamardTransform(AbstractTransform):

    def __getMatrix(self, size):
        # Generating Hadamard matrix of size 'size'
        n = int(math.log(size, 2))
        row = [1 / (np.sqrt(2) ** n) for i in xrange(0, size)]
        matrix = [list(row) for i in xrange(0, size)]
        for i in xrange(0, n):
            for j in xrange(0, size):
                for k in xrange(0, size):
                    if (j / 2 ** i) % 2 == 1 and (k / 2 ** i) % 2 == 1:
                        matrix[j][k] = -matrix[j][k]

        # Producing Walsh-Hadamard matrix by ordering frequencies in ascending order
        matrix.sort(key = lambda x: sum(map(lambda a: a[0] * a[1] < 0, zip(x[1:], x[:-1]))))
        return matrix

    def transform(self, src):
        size = src.shape[0]
        h = np.matrix(self.__getMatrix(size))
        return h * src * h

    def inverseTransform(self, src):
        return self.transform(src)
