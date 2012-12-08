__author__ = 'vio'
from Word_Graph import Graph
from sys import argv

if __name__ == "__main__":
    if len(argv) != 4:
        print argv
        print "Wrong args"
        exit()
    with open(argv[1]) as file:
        words = [line.rstrip() for line in file]
    g = Graph(words)
    print("Words : " + argv[2] + "---->" + argv[3])
    trace = g.min_trace(argv[2], argv[3])
    print(trace)
