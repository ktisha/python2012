import sys
from string import maketrans
import itertools
from collections import Counter

file_to_decode = sys.argv[1]
text_file = open(file_to_decode, 'r')
text_to_be_decoded = text_file.read()
text_to_decode = text_to_be_decoded.lower()
text_file.close()

def compare_word_statistic_to_original_dictionary (original_dic, word_statistics):
    similarity = 0
    i = 0
    while i < len(word_statistics):
        current_word = word_statistics[i][0]
        if original_dic.has_key(current_word):
            similarity += 1
        i += 1
    return similarity

def find_most_frequent_char_in_string (string_with_chars):
    max_num = 0
    max_char = ''
    for x in string_with_chars:
        if string_with_chars.count(x) > max_num:
            max_num = string_with_chars.count(x)
            max_char = x
    if max_num > len(string_with_chars)*0.5:
        return max_char
    else:
        return None

def sort_dic(dic_to_be_sorted):
    sorted_list = []
    for key, value in sorted(dic_to_be_sorted.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        sorted_list = sorted_list + [[key, value]]
    return sorted_list

def count_word_frequency (text):
    dic = {}
    for word in text.split():
        if word in dic:
            dic[word] = 1 + dic[word]
        else:
            dic[word] = 1
    return sort_dic(dic)

def count_letter_frequency (text):
    dic = dict((k, float(v)/len(text)) for k,v in Counter(text).most_common())
    return sort_dic(dic)

def count_first_word_letter_frequency (text):
    first_letters = ""
    for word in text.split():
        first_letters += word[0]
    return count_letter_frequency(first_letters)

def count_first_unique_word_letter_frequency (text):
    first_letters = ""
    for word_num in count_word_frequency(text):
        unique_word = word_num[0]
        first_letters += unique_word[0]
    return count_letter_frequency(first_letters)

def count_bigram_frequency (text):
    dic = {}
    for word in text.split():
        letter_num = 0
        while letter_num < len(word) - 1:
            bigram = word[letter_num] + word[letter_num+1]
            letter_num += 1
            if bigram in dic:
                dic[bigram] = 1 + dic[bigram]
            else:
                dic[bigram] = 1
    return sort_dic(dic)

def count_trigram_frequency (text):
    dic = {}
    for word in text.split():
        letter_num = 0
        while letter_num < len(word) - 2:
            bigram = word[letter_num] + word[letter_num+1] + word[letter_num+2]
            letter_num += 1
            if bigram in dic:
                dic[bigram] = 1 + dic[bigram]
            else:
                dic[bigram] = 1
    return sort_dic(dic)


intab  = ""
outtab = ""
alphabet = "abcdefghijklmnopqrstuvwxyz"
frequent_element = []
crypt_dic = dict()
i = 0
while i < len(alphabet):
    crypt_dic[alphabet[i]] = None
    i += 1

trigram_statistic = count_trigram_frequency (text_to_decode)
bigram_statistic = count_bigram_frequency (text_to_decode)
first_unique_word_letter_statistic = count_first_unique_word_letter_frequency (text_to_decode)
first_word_letter_statistic = count_first_word_letter_frequency (text_to_decode)
word_statistic = count_word_frequency (text_to_decode)
letter_statistic = count_letter_frequency (text_to_decode)
if letter_statistic[0][0] == ' ':
    del letter_statistic[0]


# Magic inside! Don't touch, please!

#t
current_char = ''
if len(first_word_letter_statistic) > 0:
    frequent_element = first_word_letter_statistic[0]
    current_char += frequent_element[0]
if len(letter_statistic) > 1:
    frequent_element = letter_statistic[1]
    current_char += frequent_element[0]
if len(bigram_statistic) > 0:
    frequent_element = bigram_statistic[0][0]
    current_char += frequent_element[0]
if len(trigram_statistic) > 0:
    frequent_element = trigram_statistic[0][0]
    current_char += frequent_element[0]
crypt_dic['t'] = find_most_frequent_char_in_string (current_char)

#h
current_char = ''
if len(trigram_statistic) > 0 and trigram_statistic[0][0][0] == crypt_dic['t']:
    frequent_element = trigram_statistic[0][0]
    current_char += frequent_element[1]
if len(bigram_statistic) > 0 and bigram_statistic[0][0][0] == crypt_dic['t']:
    frequent_element = bigram_statistic[0][0]
    current_char += frequent_element[1]
if len(bigram_statistic) > 1 and (bigram_statistic[1][0][0] == current_char[0] or bigram_statistic[1][0][0] == current_char[1]):
    frequent_element = bigram_statistic[1][0]
    current_char += frequent_element[0]
i = 0
while i < min(len(word_statistic), 10):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[0] == crypt_dic['t']:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['h'] = find_most_frequent_char_in_string (current_char)

#e
current_char = ''
if len(trigram_statistic) > 0 and trigram_statistic[0][0][0] == crypt_dic['t'] and trigram_statistic[0][0][1] == crypt_dic['h']:
    frequent_element = trigram_statistic[0][0]
    current_char += frequent_element[2]
if len(bigram_statistic) > 1 and bigram_statistic[1][0][0] == crypt_dic['h']:
    frequent_element = bigram_statistic[1][0]
    current_char += frequent_element[1]
if len(letter_statistic) > 0:
    frequent_element = letter_statistic[0][0]
    current_char += frequent_element
i = 0
while i < min(len(word_statistic), 10):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[0] == crypt_dic['t'] and current_word[1] == crypt_dic['h']:
        current_char += current_word[2]
        break
    i += 1
crypt_dic['e'] = find_most_frequent_char_in_string (current_char)

#a
current_char = ''
if len(letter_statistic) > 2:
    frequent_element = letter_statistic[2][0]
    current_char += frequent_element
if len(trigram_statistic) > 1:
    frequent_element = trigram_statistic[1][0]
    current_char += frequent_element[0]
i = 0
while i < min(len(bigram_statistic), 20):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[0] == crypt_dic['h'] and current_bigram[1] != crypt_dic['e']:
        current_char += current_bigram[1]
    i += 1
i = 0
while i < min(len(word_statistic), 10):
    current_word = word_statistic[i][0]
    if len(current_word) == 1:
        current_char += current_word
    i += 1
crypt_dic['a'] = find_most_frequent_char_in_string (current_char)

#n
current_char = ''
if len(trigram_statistic) > 1:
    frequent_element = trigram_statistic[1][0]
    current_char += frequent_element[1]
i = 0
while i < min(len(bigram_statistic), 10):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[0] == crypt_dic['a']:
        current_char += current_bigram[1]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 10):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[0] == crypt_dic['a']:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['n'] = find_most_frequent_char_in_string (current_char)

#d
current_char = ''
if len(trigram_statistic) > 1:
    frequent_element = trigram_statistic[1][0]
    current_char += frequent_element[2]
i = 0
while i < min(len(bigram_statistic), 20):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[0] == crypt_dic['n']:
        current_char += current_bigram[1]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 10):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[0] == crypt_dic['a'] and current_word[1] == crypt_dic['n']:
        current_char += current_word[2]
        break
    i += 1
crypt_dic['d'] = find_most_frequent_char_in_string (current_char)

#s
current_char = ''
if len(word_statistic) > 50:
    frequent_element = first_unique_word_letter_statistic[0]
    current_char += frequent_element[0]
crypt_dic['s'] = find_most_frequent_char_in_string (current_char)

#o
current_char = ''
if len(letter_statistic) > 3:
    frequent_element = letter_statistic[3][0]
    current_char += frequent_element
i = 0
while i < min(len(word_statistic), 25):
    current_word = word_statistic[i][0]
    if len(current_word) == 2 and current_word[0] == crypt_dic['t']:
        current_char += current_word[1]
        break
    i += 1
i = 0
while i < min(len(trigram_statistic), 30):
    current_trigram = trigram_statistic[i][0]
    if current_trigram[0] == crypt_dic['n'] and current_trigram[2] == crypt_dic['t']:
        current_char += current_trigram[1]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 15):
    current_word = word_statistic[i][0]
    if len(current_word) == 2 and current_word[0] == crypt_dic['t']:
        current_char += current_word[1]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 30):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[0] == crypt_dic['n'] and current_word[2] == crypt_dic['t']:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['o'] = find_most_frequent_char_in_string (current_char)

#i
current_char = ''
i = 0
while i < min(len(word_statistic), 30):
    current_word = word_statistic[i][0]
    if len(current_word) == 1 and current_word != "a":
        current_char += current_word
        break
    i += 1
i = 0
while i < min(len(bigram_statistic), 10):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[1] == crypt_dic['n'] and current_bigram[0] != crypt_dic['a'] and current_bigram[0] != crypt_dic['o'] and current_bigram[0] != crypt_dic['e']:
        current_char += current_bigram[0]
        break
    i += 1
i = 0
while i < min(len(trigram_statistic), 10):
    current_trigram = trigram_statistic[i][0]
    if current_trigram[1] == crypt_dic['n'] and current_bigram[0] != crypt_dic['a']:
        current_char += current_bigram[0]
        break
    i += 1
crypt_dic['i'] = find_most_frequent_char_in_string (current_char)

#r
current_char = ''
i = 0
while i < min(len(trigram_statistic), 30):
    current_trigram = trigram_statistic[i][0]
    if current_trigram[0] == crypt_dic['e'] and current_trigram[2] == crypt_dic['e']:
        current_char += current_trigram[1]
        break
    i += 1
i = 0
while i < min(len(bigram_statistic), 15):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[0] == crypt_dic['e']:
        current_char += current_bigram[1]
        break
    i += 1
i = 0
while i < min(len(bigram_statistic), 15):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[1] == crypt_dic['e'] and current_bigram[0] != crypt_dic['h']:
        current_char += current_bigram[0]
        break
    i += 1
crypt_dic['r'] = find_most_frequent_char_in_string (current_char)

#f
current_char = ''
i = 0
while i < min(len(trigram_statistic), 30):
    current_trigram = trigram_statistic[i][0]
    if current_trigram[1] == crypt_dic['o'] and current_trigram[2] == crypt_dic['r']:
        current_char += current_trigram[0]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 30):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[1] == crypt_dic['o'] and current_word[2] == crypt_dic['r']:
        current_char += current_word[0]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 30):
    current_word = word_statistic[i][0]
    if len(current_word) == 2 and current_word[0] == crypt_dic['o'] and current_word[1] != crypt_dic['n']:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['f'] = find_most_frequent_char_in_string (current_char)

#g
current_char = ''
i = 0
while i < min(len(trigram_statistic), 10):
    current_trigram = trigram_statistic[i][0]
    if current_trigram[0] == crypt_dic['i'] and current_trigram[1] == crypt_dic['n']:
        current_char += current_trigram[2]
        break
    i += 1
crypt_dic['g'] = find_most_frequent_char_in_string (current_char)

#w
current_char = ''
i = 0
while i < min(len(word_statistic), 50):
    current_word = word_statistic[i][0]
    if len(current_word) == 4 and current_word[1] == crypt_dic['i'] and current_word[2] == crypt_dic['t'] and current_word[3] == crypt_dic['h']:
        current_char += current_word[0]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 40):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[1] == crypt_dic['a'] and current_word[2] == crypt_dic['s'] and current_word[0] != crypt_dic['h']:
        current_char += current_word[0]
        break
    i += 1
crypt_dic['w'] = find_most_frequent_char_in_string (current_char)

#m
current_char = ''
i = 0
while i < min(len(word_statistic), 50):
    current_word = word_statistic[i][0]
    if len(current_word) == 4 and current_word[0] == crypt_dic['f'] and current_word[1] == crypt_dic['r'] and current_word[2] == crypt_dic['o']:
        current_char += current_word[3]
        break
    i += 1
crypt_dic['m'] = find_most_frequent_char_in_string (current_char)

#u
current_char = ''
i = 0
while i < min(len(bigram_statistic), 50):
    current_bigram = bigram_statistic[i][0]
    if current_bigram[0] == crypt_dic['o'] and current_bigram[1] != crypt_dic['n'] and current_bigram[1] != crypt_dic['r'] and current_bigram[1] != crypt_dic['f']:
        current_char += current_bigram[1]
        break
    i += 1
crypt_dic['u'] = find_most_frequent_char_in_string (current_char)

#b
current_char = ''
i = 0
while i < min(len(word_statistic), 100):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[1] == crypt_dic['u'] and current_word[2] == crypt_dic['t'] and current_word[2] != crypt_dic['o']:
        current_char += current_word[0]
        break
    i += 1
crypt_dic['b'] = find_most_frequent_char_in_string (current_char)

#l
current_char = ''
i = 0
while i < min(len(word_statistic), 70):
    current_word = word_statistic[i][0]
    if len(current_word) == 3 and current_word[0] == crypt_dic['a'] and current_word[1] == current_word[2]:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['l'] = find_most_frequent_char_in_string (current_char)

#v
current_char = ''
i = 0
while i < min(len(word_statistic), 100):
    current_word = word_statistic[i][0]
    if len(current_word) == 4 and current_word[0] == crypt_dic['h'] and current_word[1] == crypt_dic['a'] and current_word[3] == crypt_dic['e']:
        current_char += current_word[2]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 100):
    current_word = word_statistic[i][0]
    if len(current_word) == 4 and current_word[0] == crypt_dic['e'] and current_word[2] == crypt_dic['e'] and current_word[3] == crypt_dic['r']:
        current_char += current_word[1]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 100):
    current_word = word_statistic[i][0]
    if len(current_word) == 4 and current_word[0] == crypt_dic['e'] and current_word[2] == crypt_dic['e'] and current_word[3] == crypt_dic['n']:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['v'] = find_most_frequent_char_in_string (current_char)

#y
current_char = ''
i = 0
while i < min(len(word_statistic), 50):
    current_word = word_statistic[i][0]
    if len(current_word) == 2 and current_word[0] == crypt_dic['m'] and current_word[1] != crypt_dic['e']:
        current_char += current_word[1]
        break
    i += 1
crypt_dic['y'] = find_most_frequent_char_in_string (current_char)

#p
current_char = ''
i = 0
while i < min(len(word_statistic), 100):
    current_word = word_statistic[i][0]
    if len(current_word) == 2 and current_word[0] == crypt_dic['u'] and current_word[1] != crypt_dic['s']:
        current_char = current_word[1]
        break
    i += 1
i = 0
while i < min(len(word_statistic), 100):
    current_word = word_statistic[i][0]
    if len(current_word) == 4 and current_word[0] == crypt_dic['u'] and current_word[2] == crypt_dic['o'] and current_word[2] == crypt_dic['n']:
        current_char = current_word[1]
        break
    i += 1
crypt_dic['p'] = find_most_frequent_char_in_string (current_char)

#c
current_char = ''
i = 0
while i < min(len(trigram_statistic), 30):
    current_trigram = trigram_statistic[i][0]
    if current_trigram[0] == crypt_dic['n'] and current_trigram[2] == crypt_dic['e']:
        current_char += current_trigram[1]
        break
    i += 1
crypt_dic['c'] = find_most_frequent_char_in_string (current_char)

original_dictionary_file = open("./1000_most_used_words_by_rank.txt", 'r')

original_dictionary_list = original_dictionary_file.read()
original_dictionary_file.close()
original_dictionary = dict()
for word in original_dictionary_list.split():
    original_dictionary[word] = None

undefined_letters = ""
for key in crypt_dic.iterkeys():
    if crypt_dic[key] == None:
        undefined_letters += key
    else:
        outtab += key
        intab += crypt_dic[key]

outtab += undefined_letters
best_fit = ""
max_sim = 0
letters_for_permutations = ""

for letter in alphabet:
    if intab.count(letter) == 0:
        letters_for_permutations += letter

for current_permutation in list(map("".join, itertools.permutations(letters_for_permutations))):
    intab = intab [0:(len(alphabet) - len(undefined_letters))] + current_permutation
    print intab + " " + outtab
    trantab = maketrans(intab, outtab)
    decoded_text = text_to_decode.translate(trantab)
    sim_num = compare_word_statistic_to_original_dictionary (original_dictionary, count_word_frequency(decoded_text))
    print sim_num
    if sim_num > max_sim:
        max_sim = sim_num
        best_fit = intab

trantab = maketrans(best_fit, outtab)
result_text = text_to_decode.translate(trantab)

output_file = open('./output.txt','w')
output_file.write(result_text)
output_file.close

print "result trantab:"
print outtab
print intab
print max_sim
