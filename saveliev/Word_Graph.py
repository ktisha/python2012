__author__ = 'vio'
from collections import deque
class Vertex:
    def __init__(self, word):
        self.word = word
        self.edges = []
        self.used = False
        self.from_vertex = None
        self.distance = 0
    def add_edge(self, vertex):
        self.edges.append(vertex)
        vertex.edges.append(self)

class Graph:
    def __init__(self, word_list):
        self.vertexes = []

        words = tuple( {word for word in word_list} )
        word_len = len(words[0])
        n = len(words)

        for word in words:
            self.vertexes.append(Vertex(word[:word_len]))

        for i in range(n - 1):
            for j in range(i + 1, n):
                diff_count = 0
                for k in range(word_len):
                    if words[i][k] != words[j][k]:
                        diff_count += 1
                        if diff_count > 1:
                            break
                if diff_count == 1:
                    self.vertexes[i].add_edge(self.vertexes[j])

    def min_trace(self, start_word, end_word):
        start = end = None
        for vertex in self.vertexes:
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
                    v.distance = vertex.distance + 1
                    v.from_vertex = vertex
                    queue_len += 1
        trace = []
        current_vertex = end

        while current_vertex is not None:
            trace.append(current_vertex)
            current_vertex = current_vertex.from_vertex
        trace.reverse()
        return [] if len(trace) == 0 or trace[0] != start else [vertex.word for vertex in trace]





