__author__ = 'Kirill Kononov, Sergey Karashevich'

import re, os
from os.path import join

class Parser:

    def __init__(self, proclogFileName):
        self.proclog = list()
        self.info = dict()

        with open(proclogFileName, 'r') as input_file:
            for line in input_file:
                self.proclog.append(line)


    def parse(self, info_prefix, info_id, info_postfix):
        for line in self.proclog:
            name_prefix = re.search(info_prefix + "\s*", line)

            if name_prefix:
                name = line[name_prefix.end() : line.find(info_postfix, name_prefix.end())]
                self.info[info_id] = name.strip()

                return

    def printParser(self):
        for k, v in self.info.iteritems():
            print k + " " * (20 - len(k)) + "\"" + v + "\""

    def fillDict(self):
        self.parse("Processing image \"", "IMG_NAME", "\"")
        self.parse("exposure =", "EXPOSURE", "s")
        self.parse("CCD temperature =", "CCD_TEMP", "K")
        self.parse("filter \"", "FILTER", "\"")
        self.parse("Observation target:", "OBJECT", "\n")
        self.parse("Mid-exposure time:", "EXPTIME", "UTC")
        self.parse("Latitude:", "LAT", "\n")
        self.parse("Longitude:", "LONG", "\n")
        self.parse("Altitude:", "ALT", "m")
        self.parse("Reference catalog:", "CAT_ASTR", "\n")
        self.parse("Image center RA", "IMG_CENTER_RA", "  ")
        self.parse("Image center Dec", "IMG_CENTER_DEC", "  ")

    def process(self):
        self.fillDict()
        self.printParser()


def isProclog(str):
    if str.endswith(".proclog"):
        return True
    else:
        return False


def main():

    for root, dirs, files in os.walk("."):
        for name in files:
            if isProclog(name):
                print (join(root, name))
                parser = Parser(join(root, name))
                parser.process()
                del parser

main()