__author__ = 'vio'
import random
import time
from collections import deque
import profile
import pstats

class Vertex:
    def __init__(self, word):
        self.word = word
        self.edges = []
        self.used = False
        self.from_vertex = None
        self.d = 0
    def add_edge(self, vertex):
        self.edges.append(vertex)
        vertex.edges.append(self)

class Graph:
    def __init__(self, dict_file_name):
        self.vertexes = []

        with open(dict_file_name) as file:
            words = {line for line in file}

        words = tuple(words)
        word_len = len(words[0]) - 1
        n = len(words)

        for word in words:
            self.vertexes.append(Vertex(word[:word_len]))

        for i in xrange(n - 1):
            for j in xrange(i + 1, n):
                diff_count = 0
                for k in xrange(word_len):
                    if words[i][k] != words[j][k]:
                        diff_count += 1
                        if diff_count > 1:
                            break
                if diff_count == 1:
                    self.vertexes[i].add_edge(self.vertexes[j])

def gen_big_dict(dict_file_name, words_count, word_len):
    file = open(dict_file_name, "w")
    word = [chr(random.randint(65, 70)) for i in xrange(word_len)]
    for i in xrange(words_count):
        for j in xrange(3):
            word[random.randint(0, word_len - 1)] = chr(random.randint(65, 70))
        file.write(''.join(word) + '\n')
    file.close()

def min_trace(graph, start_word, end_word):
    start = end = None
    for vertex in graph.vertexes:
        if vertex.word == start_word:
            start = vertex
        if vertex.word == end_word:
            end = vertex
    if start is None or end is None:
        return []
    queue = deque([start])
    queue_len = 1
    start.used = True
    while queue_len > 0:
        vertex = queue.popleft()
        queue_len -= 1
        for v in vertex.edges:
            if not v.used:
                v.used = True
                queue.append(v)
                v.d = vertex.d + 1
                v.from_vertex = vertex
                queue_len += 1
    trace = []
    current_vertex = end

    while current_vertex is not None:
        trace.append(current_vertex)
        current_vertex = current_vertex.from_vertex
    trace.reverse()
    return [] if len(trace) == 0 or trace[0] != start else [vertex.word for vertex in trace]

def main():
    words = main.words
    t = time.time()
    g = Graph("mega_words.txt")
    print(time.time() - t)
    print("Words = " + words[0] + "---->" + words[50])
    t = time.time()
    trace = min_trace(g, words[0], words[50])
    print(time.time() - t)
    print(trace)

def prof():
    profile.run('main()', 'main_prof')
    stats = pstats.Stats('main_prof')
    stats.strip_dirs()
    stats.sort_stats('time')
    stats.print_stats(7)

if __name__ == "__main__":
    gen_big_dict("mega_words.txt", 10000, 10)
    with open("mega_words.txt") as file:
        wordSet = {line.rstrip() for line in file}
    main.words = tuple(wordSet)
    prof()