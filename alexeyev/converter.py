__author__ = 'Anton M Alexeyev'
# I decided to implement HAL, not SAM -- another method for cognitive studies and recommender systems

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from matrix_management import WordMatrix
import re
import nltk

# todo: filter after processing
# todo: pucntuation + not-a-word tokens to be thrown away (regexp probably)

input_text = open("testtext", "r")
text = ""

for line in input_text:
    text += line.lower() + " "

print "Text loaded"

# maybe should first do sent_tokenize, then word_tokenize

# i chose the one everybody knows
stemmer = PorterStemmer()

# dumb tokenization
tokens = re.findall(r"[A-Za-z]+", text)
print "Tokens set built :", tokens

# stemming
#normalized_tokens = [stemmer.stem(token) for token in tokens if token not in stopwords.words('english')]
normalized_tokens = [stemmer.stem(token) for token in tokens]

print "Tokens set filtered and stemmed :", normalized_tokens

window_size = 10
matrix = WordMatrix()

win_start = 0
while win_start + window_size <= len(normalized_tokens):
    window = normalized_tokens[win_start:win_start + window_size]
    first = 0
    second = 1
    while first < len(window):
        second = first + 1
        while second < len(window):
            matrix.add(window[first], window[second], window_size - second + first + 1)
            second += 1
        first += 1
    win_start += 1

print "Co-occurence counted"
print "Keys quantity:", len(matrix.get_tokens())
# todo: tabs stuff, cool printing
#s = "    "
#
#s += " " + " ".join(matrix.get_tokens())

for key in matrix.get_tokens():
    if not key in stopwords.words('english'):
        print key, matrix.kn_cooccurences(key, 6)

print "Now to more sophisticated analysis"

for key in matrix.get_tokens():
    if not key in stopwords.words('english'):
        print key, matrix.kn_columns(key, 6, matrix.dist_cols_euclidean)

print "Done"

"""
for token0 in matrix.get_tokens():
    s += "\n" + token0
    for token1 in matrix.get_tokens():
        s += " " + str(matrix.get(token0, token1))

print s
"""