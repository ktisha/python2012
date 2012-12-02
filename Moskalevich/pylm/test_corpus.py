__author__ = 'Pavel Moskalevich'

import unittest
from corpus import Reader

class TestReader(unittest.TestCase):
#    def setUp(self):
#        pass

    def test_read(self):
#        tc = unittest.TestCase()
        reader = Reader("test\\data", "*.txt")
        for file in reader:
            print file
        self.assertIn('test\\data\\hobbit.txt', reader)
        self.assertIn('test\\data\\subdir\\dorian_gray.txt', reader)
        self.assertIn('test\\data\\subdir\\tom_sawyer.txt', reader)
        self.assertNotIn('test\\data\\garbage.log', reader)
        self.assertNotIn('test\\data\\subdir\\just_txt', reader)

if __name__ == '__main__':
    unittest.main()