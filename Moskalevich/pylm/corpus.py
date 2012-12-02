__author__ = 'Pavel Moskalevich'

from fnmatch import fnmatch
from os.path import isdir
from os import walk

class Reader:
    ''' This class contains a number of files, which are then
    read one by one.
    '''

    def __init__(self, path, pattern = '*.txt'):
        self.files = []
        self.add_files(path, pattern)

    def add_files(self, path, pattern):
        if not isdir(path):
            return
        for root, dirs, files in walk(path):
            matched_files = filter(lambda x: fnmatch(x, pattern), files)
            matched_files = map(lambda x: path.join(root, x), matched_files)
            self.files.extend(matched_files)

    def __iter__(self):
        return self.files

