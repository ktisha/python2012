#!/usr/bin/python
#-*- coding: utf-8 -*-
__author__ = 'Anton M Alexeyev'
# I decided to implement HAL -- a method for cognitive studies and recommender systems

from nltk.stem import PorterStemmer
from hashed_matrix_management import HashedWordMatrix
from nltk.corpus import stopwords
from nltk import pos_tag
import re
from data_printer import graph_to_file


window_size = 11
min_freq = 11
matrix = HashedWordMatrix()

# i chose the one everybody knows
stemmer = PorterStemmer()

def train_model(file):
    global matrix
    global stemmer
    global window_size
    global min_freq

    charlist = ["alice", "cat", "gryphon",
                "hatter", "mouse", "dodo", "time",
                "duchess", "dormouse", "queen",
                "rabbit", "king", "turtle", "pigeon"]

    matrix = HashedWordMatrix()

    print "Loading text..."

    input_text = open(file, "r")
    text = ""

    for line in input_text:
        text += line.lower() + " "

    input_text.close()

    print "Tokenization..."

    tokens = re.findall(r"[A-Za-z]+", text)

    print "POS-tagging..."

    tagged_tokens = pos_tag(tokens)

    print "Stop-words filtering..."

    tokens_filtered = []
    for pair in tagged_tokens:
        if pair[0] in stopwords.words('english'):
            tokens_filtered += [("*", pair[1])]
        else:
            tokens_filtered += [ pair ]

    tokens_filtered = [('*', "-NONE-")] * (window_size - 1) + tokens_filtered + [('*', "-NONE-")] * (window_size - 1)

    print "Stemming..."

    normalized_pairs = [(stemmer.stem(pair[0]), pair[1]) for pair in tokens_filtered]

    print "Frequential filtering..."

    dict = {}
    for pair in normalized_pairs:
        if not dict.has_key(pair[0]):
            dict[pair[0]] = 0
        dict[pair[0]] += 1

    normalized_tokens = []

    for pair in normalized_pairs:
        if dict[pair[0]] < min_freq or pair[0] == "*":
            normalized_tokens += ['*' + pair[1]]
        else:
            normalized_tokens += [pair[0]]

    print "Learning..."

    win_start = 0
    while win_start + window_size <= len(normalized_tokens):
        window = normalized_tokens[win_start:win_start + window_size]
        first = 0
        second = 1
        while first < len(window):
            second = first + 1
            while second < len(window):
               matrix.add(window[first], window[second], 1)
               second += 1
            first += 1
        win_start += 1

    print "Normalization..."

    matrix.normalize()

    print "Number of terms:", str(len(matrix.get_tokens())) + "."

    print "Writing graph to file"

    graph_to_file(matrix, charlist, 'graph.nwb')

    print "Done."

def get_token_by_word(word):
    global stemmer
    word = re.findall(r"[A-Za-z]+", word)[0]
    return stemmer.stem(word.lower())

def get_euclidean_vector_by_token(n, token):
    global matrix
    print "New token:", token
    if token in matrix.get_tokens():
        return matrix.kn_columns(token, n, matrix.dist_cols_euclidean)
    raise KeyError

def get_cosine_vector_by_token( n, token):
    global matrix
    print "New token:", token
    if token in matrix.get_tokens():
        return matrix.kn_columns(token, n, matrix.dist_cols_inverted_cosine)
    raise KeyError

def get_frequential_vector_by_token(n, token):
    global matrix
    print "New token:", token
    if token in matrix.get_tokens():
        return matrix.kn_cooccurences(token, n)
    raise KeyError

def get_manhattan_vector_by_token(n, token):
    global matrix
    print "New token:", token
    if token in matrix.get_tokens():
        return matrix.kn_columns(token, n, matrix.dist_cols_manhattan)
    raise KeyError

def test_print():
    global matrix
    for key in matrix.get_tokens():
        print key,
        for succ in matrix.get_tokens():
            print matrix.get(key, succ),
        print