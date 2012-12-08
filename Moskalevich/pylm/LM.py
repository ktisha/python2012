__author__ = 'Pavel Moskalevich'

from sys import argv
from corpus import Reader
from text import Normalizer, NgramMaker
from smoothing import GoodTuring
from math import log10

def main(args):
    corpus    = '.'
    outFile   = 'lm.txt'
    max_order = 3
    gtNmin    = [1,1,1]

    for i in xrange(0, len(args)):
        if args[i] == '-c':
            corpus    = args[i + 1]
        elif args[i] == '-lm':
            outFile   = args[i + 1]
        elif args[i] == '-o':
            max_order = args[i + 1]
        elif args[i] == '-gt':
            nums = args[i + 1].split(',')
            gtNmin = map(lambda n: int(n), nums)

    if max_order <= 0:
        print "Max order must be non-negative"
        exit(1)

    reader   = Reader(corpus)
    ng_maker = NgramMaker(max_order)

    for file in reader:
        ng_maker.parse(Normalizer.normalize(file))

    gt = GoodTuring(ng_maker.storage(), gtNmin)
    ng_storage = gt.storage()

    out_file = open(outFile, 'w')
    out_file.write('\\data\\\n\n')
    for ng_ord in xrange(1, ng_storage.max_order() + 1):
        out_file.write("ngram %d=%d\n" % (ng_ord, ng_storage.distinct_n_grams(ng_ord)))

    for ng_ord in xrange(1, ng_storage.max_order() + 1):
        out_file.write('\n\\%d-grams:\n' % ng_ord)
        for ng in sorted(ng_storage.get_n_grams(ng_ord)):
            ngram = ng_storage.get_n_gram(ng)
            if ng_ord < ng_storage.max_order():
                out_file.write("%.8f\t%s\t0\n" % (ngram.prob, ' '.join(ng)))
            else:
                out_file.write("%.8f\t%s\n" % (ngram.prob, ' '.join(ng)))

    out_file.write('\n\\end\\\n')
    out_file.close()


if __name__ == '__main__':
    main(argv[1:])