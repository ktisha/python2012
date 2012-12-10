import csv
import sys
import re
from collections import Counter

def read_characters(filename):
	all_characters = []
	characters = open(filename)
	for char in characters.read():
		all_characters += [char.lower()]
	return all_characters

def get_list(items,pattern):
	filtered_list = []
	for item in items:
		m = pattern.search(str(item))
		if (not(m==None)):
			filtered_list += [item]
	return filtered_list

def all_letters_frequency(filename):
	one_letter_pattern = re.compile('[a-zA-Z]')
	all_characters = read_characters(filename)
	all_letters = get_list(all_characters,one_letter_pattern)
	count = Counter(all_letters)
	common = count.most_common()
	return common

def all_double_letters_frequency(filename):
	double_letter_pattern = re.compile(r"(.)\1")
	all_characters = read_characters(filename)
	pairs_of_char = [i+j for i,j in zip(all_characters[::2],all_characters[1::2])]
	pairs_of_char = pairs_of_char + [i+j for i,j in zip(all_characters[1::2],all_characters[2::2])]
	all_pairs = get_list(pairs_of_char,double_letter_pattern)
	count = Counter(all_pairs)
	common = count.most_common()
	return common

def all_capital_letters_frequency(filename):
	capital_letter_pattern = re.compile('[A-Z]')
	all_characters = read_characters(filename)
	all_letters = get_list(all_charaters,one_letter_pattern)
	count = Counter(all_letters)
	common = count.most_common()
	return common

def all_pairs_of_letter_frequency(filename):
	pair_of_letter_pattern = re.compile('[a-zA-Z]+[a-zA-Z]')
	all_characters = read_characters(filename)
	pairs_of_char = [i+j for i,j in zip(all_characters[::2],all_characters[1::2])]
	pairs_of_char = pairs_of_char + [i+j for i,j in zip(all_characters[1::2],all_characters[2::2])]
	all_pairs = get_list(pairs_of_char,pair_of_letter_pattern)
	count = Counter(all_pairs)
	common = count.most_common()
	return common

def all_letter_begin_with_frequency(filename):
	begin_with_pattern = re.compile('[\s]+[a-zA-Z]')
	all_characters = read_characters(filename)
	pairs_of_char = [i+j for i,j in zip(all_characters[::2],all_characters[1::2])]
	pairs_of_char = pairs_of_char + [i+j for i,j in zip(all_characters[1::2],all_characters[2::2])]
	all_pairs = get_list(pairs_of_char,begin_with_pattern)
	count = Counter(all_pairs)
	common = count.most_common()
	return common

def all_letter_end_with_frequency(filename):
	end_with_pattern = re.compile('[a-zA-Z]+[\s]')
	all_characters = read_characters(filename)
	pairs_of_char = [i+j for i,j in zip(all_characters[::2],all_characters[1::2])]
	pairs_of_char = pairs_of_char + [i+j for i,j in zip(all_characters[1::2],all_characters[2::2])]
	all_pairs = get_list(pairs_of_char,end_with_pattern)
	count = Counter(all_pairs)
	common = count.most_common()
	return common
