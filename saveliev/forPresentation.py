__author__ = 'vio'
import random
import time
from Word_Graph import Graph
def gen_big_dict(dict_file_name, words_count, word_len):
    file = open(dict_file_name, "w")
    word = [chr(random.randint(65, 70)) for i in range(word_len)]
    for i in range(words_count):
        for j in range(3):
            word[random.randint(0, word_len - 1)] = chr(random.randint(65, 70))
        file.write(''.join(word) + '\n')
    file.close()

def constructGraph(start, end):
    g = Graph(words)
    print("Words : " + start + "---->" + end)
    trace = g.min_trace(start, end)
    print(trace)

if __name__ == "__main__":
    #gen_big_dict("mega_words.txt", 3000, 5)
    with open("mega_words.txt") as file:
        words = [line.rstrip() for line in file]
    t = time.time()
    constructGraph(words[0], words[50])
    #['DBDEA', 'CBDEA', 'CBDAA', 'CBDAE', 'CADAE', 'BADAE']
    print("Work time :" + str(time.time() - t))
