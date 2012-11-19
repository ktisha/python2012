__author__ = 'Anton M Alexeyev'
# I decided to implement HAL, not SAM -- another method for cognitive studies and recommender systems

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from matrix_management import WordMatrix

# todo: filter after processing
# todo: pucntuation + not-a-word tokens to be thrown away (regexp probably)
# todo: text = text.lower()?
stopwords = []

text = "What goes around comes around"
print "Initial text: " + text
print

# maybe should first do sent_tokenize, then word_tokenize
tokens = word_tokenize(text)
normalized_tokens = []

# i chose the one everybody knows
stemmer = PorterStemmer()

# tokenization and stemming
for token in tokens:
    normalized_tokens += [stemmer.stem(token)]

window_size = 5

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

# todo: tabs stuff, cool printing
s = "    "

s += " " + " ".join(matrix.get_tokens())

for token0 in matrix.get_tokens():
    s += "\n" + token0
    for token1 in matrix.get_tokens():
        s += " " + str(matrix.get(token0, token1))

print s