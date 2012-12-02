__author__ = 'Pavel Moskalevich'

from fnmatch import fnmatch
from os import path
from os import walk

class Reader:
    ''' This class contains a number of files, which are then
    read one by one.
    '''

    def __init__(self, folder, pattern = '*.txt'):
        self.files = []
        self.add_files(folder, pattern)

    def add_files(self, folder, pattern):
        if not path.isdir(folder):
            return
        for root, dirs, files in walk(folder):
            matched_files = filter(lambda x: fnmatch(x, pattern), files)
            matched_files = map(lambda x: path.join(root, x), matched_files)
            self.files.extend(matched_files)

    def __iter__(self):
        return self.files.__iter__()

