__author__ = 'sergio'

import sys

MAX_DEPTH = 50
MAX_CIPHER_WORDS = 500

def input_text(filename):
    result = []
    with open(filename, "r") as f:
        for line in f:
            result.append(line)
    return result

def text_to_words(text):
    result = []
    for line in text:
        # TODO: filter non-letters: filter(lambda x: x in 'a-z', line)
        for word in line.split():
            result.append(word)
    return  result

def decode(chipher_text, decoder):
    result = ''
    for line in chipher_text:
        for char in line:
            result += decoder[char] if char in decoder else '*' \
                                    if char != ' ' and char !='\n' else char
    return result

def make_pattern_sets(frequent_words, cipher_words):
    result = {}
    for cipher_word in cipher_words:
        set = {}
        for frequent_word in frequent_words:
            if match(frequent_word, cipher_word):
                set[frequent_word] = True
        if len(set) > 0:
            result[cipher_word] = set
    return result

def distinct_letters(word):
    letters = {}
    for letter in word:
        letters[letter] = True
    return letters

def sort_cipher_words(cipher_words, pattern_sets):
    rest_cipher_words = {word for word in cipher_words}
    result_len = len(rest_cipher_words)
    result = []
    common_letters = {}

    # take first word
    cipher_words_with_rating = [(word, len(pattern_sets[word]) / len(distinct_letters(word))) \
                                for word in cipher_words]
    cipher_words_with_rating.sort(key = lambda x: x[1])
    first_word = cipher_words_with_rating[0][0]
    common_letters.update(distinct_letters(first_word))
    result.append(first_word)
    rest_cipher_words.remove(first_word)

    # take other words
    while len(result) < result_len:
        last_common_letters_count = -1
        last_word_length = -1
        for word in rest_cipher_words:
            common_letters_count = len([letter for letter in distinct_letters(word) \
                                        if letter in common_letters])
            if (common_letters_count > last_common_letters_count) or \
                ((common_letters_count == last_common_letters_count) and \
                    len(word) > last_word_length):
                last_common_letters_count = common_letters_count
                last_word_length = len(word)
                saved_word = word
            # TODO: if there no common letters at all ?
        common_letters.update(distinct_letters(saved_word))
        result.append(saved_word)
        rest_cipher_words.remove(saved_word)

    return result


def match(w1, w2):
    if len(w1) != len(w2):
        return False;
    for i in range(1, len(w1)):
        for j in range (i):
            if (w1[i] == w1[j]) != (w2[i] == w2[j]):
                return False
    return True

def solve(pattern_sets, order, cipher_text):

    best_f = {}
    best_f_score = 0
    MAX_DEPTH = len(order)


    def make_new_partial_permutation(f, cipher_word, decipher_word):
        f_new ={}
        f_new['cipher'] =f['cipher'].copy()
        f_new['decipher'] =f['decipher'].copy()
        assert len(cipher_word) == len(decipher_word) # "bad parameters: not equal lenghts"
        for i in range(len(cipher_word)):
            c = cipher_word[i]
            d = decipher_word[i]
            f_new['cipher'][d] = c
            f_new['decipher'][c] = d
        return f_new

    def consistent(f, cipher_word, decipher_word):
        assert len(cipher_word) == len(decipher_word) # "bad parameters: not equal lenghts"
        for i in range(len(cipher_word)):
            c = cipher_word[i]
            d = decipher_word[i]
            if d in f['cipher'] and f['cipher'][d] != c: return False
            if c in f['decipher'] and f['decipher'][c] != d: return False
        return True

    def compare_score(score, f):
        nonlocal best_f
        nonlocal  best_f_score
        nonlocal cipher_text
        if score > best_f_score:
            best_f = f.copy()
            best_f_score = score
            print ("current score = ", score)
            decoded_text = decode(cipher_text, best_f['decipher'])
            print(decoded_text)
            if score == MAX_DEPTH:
                print ("finish!")
                exit()


    def depth_search(depth, f, score):
        if score + MAX_DEPTH - depth < best_f_score or depth == MAX_DEPTH:
            compare_score(score, f)
            return
        current_word = order[depth]
        set = pattern_sets[order[depth]]
        for x in set:
            if consistent(f, current_word, x):
                f_new = make_new_partial_permutation(f, current_word, x)
                depth_search(depth + 1, f_new, score + 1)
        depth_search(depth + 1, f, score)
        return

    print("max_score = max_depth = ", MAX_DEPTH)
    f = {'cipher' : {}, 'decipher' : {}}
    depth_search(0, f, 0)
    return

if __name__ == "__main__":

    print("read frequent words base ...")
    frequent_words = text_to_words(input_text(sys.argv[1]))

    print("read cipher ...")
    cipher_text = input_text(sys.argv[2])
    cipher_words = text_to_words(cipher_text)[:MAX_CIPHER_WORDS]

    print("create patterns ...")
    pattern_sets = make_pattern_sets(frequent_words, cipher_words)

    print("clean cipher ...")
    # remove duplicates from cipher_words
    cipher_words_dict = {word: True for word in cipher_words}
    cipher_words = [word for word in cipher_words_dict]

    # remove words without pattern in pattern_sets
    cipher_words = [word for word in cipher_words if word in pattern_sets]

    print("sort cipher words ...")
    order = sort_cipher_words(cipher_words, pattern_sets)[:MAX_DEPTH]

    print("solve ...")
    solve(pattern_sets, order, cipher_text)