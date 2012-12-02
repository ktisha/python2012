__author__ = 'happy'

import fnmatch.fnmatch
import os.path.isdir
import os.walk

class Reader:
    ''' This class contains a number of files, which are then
    read one by one.
    '''

    def __init__(self, path, pattern = '*\\.txt'):
        self.files = []
        self.add_files(path, pattern)

    def add_files(self, path, pattern):
        if not os.path.isdir(path):
            return
        for root, dirs, files in os.walk(path):
            matched_files = filter(lambda x: fnmatch.fnmatch(x, pattern), files)
            self.files.extend(matched_files)

    def __iter__(self):
        return self.files

