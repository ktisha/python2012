__author__ = 'Pavel Moskalevich'

#if __name__ == "__main__" and __package__ is None:
#    __package__ = "pylm.test.test_corpus"

from corpus import Reader

reader = Reader("test\data", "*.txt")
for file in reader:
    print file