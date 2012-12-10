import sys

class Ladder:

    def __init__(self, filename):
        countLines = 0
        wordSet = set()
        with open(filename, "r") as file:
            for line in file:
                line = line.rstrip()
                countLines += 1
                if (countLines > 2):
                    if (len(self.srcWord) is not len(self.destWord)):
                        print "length of words are different"
                        exit(1)
                    lengthOfWord = len(self.srcWord)
                    if (len(line) is not lengthOfWord):
                        print "wrong length. Do not add this word"
                        print "continue read words"
                    wordSet.add(str(line).lower())
                elif (countLines == 1):
                    self.srcWord = str(line).lower()
                elif (countLines == 2):
                    self.destWord = str(line).lower()
                else:
                    print "no this situation"
                    exit(1)
        print wordSet
        print self.srcWord
        print self.destWord
        self.graph = list()
        self.answer = list()
        self.vertexCount = len(wordSet)
        print self.vertexCount
        for word in wordSet:
            self.graph.append(word)
        print self.graph

    class Node:
        def __init__(self, word, number):
            self.word = word
            self.number = number
            self.previousNode = -1
            self.nodeList = list()
            self.time = -1

        def __str__(self):
            return str(self.word)

    def buildGraph(self):
        for i in xrange(self.vertexCount):
            thisWord = str(self.graph[i])
            self.graph[i] = self.Node(thisWord, i)
            for j in xrange(self.vertexCount):
                currentWord = str(self.graph[j])
                if (differentOneSymbol(thisWord, currentWord) is True):
                    self.graph[i].nodeList.append(j)
        for v in self.graph:
            print v
            print v.number
            print v.nodeList
            print " "

    def searchChainOfWords(self):
        oldFront = list()
        sourceVertexes = list()
        newFront = list()
        destinationVertexes = list()
        currentTime = 0
        for vertex in self.graph:
            if (differentOneSymbol(self.srcWord, str(vertex)) is True):
                sourceVertexes.append(vertex)
                vertex.time = 0
            if (differentOneSymbol(self.destWord, str(vertex)) is True):
                destinationVertexes.append(vertex)
        oldFront = sourceVertexes
        findAnswer = True
        while(findAnswer):
            for vertex in oldFront:
                for adjacentVertex in vertex.nodeList:
                    v = self.graph[adjacentVertex]
                    if v.time == -1:
                        v.time = currentTime + 1
                        v.previousNode = vertex.number
                        newFront.append(v)
            if len(newFront) == 0:
                print "no chain of words"
                findAnswer = False
            for destVertex in destinationVertexes:
                if (destVertex in newFront):
                    print "Ok "
                    self.answer.append(destVertex)
                    thisTime = destVertex.time
                    thisVertex = destVertex
                    while (thisTime > 0):
                        thisVertex = self.graph[thisVertex.previousNode]
                        thisTime = thisVertex.time
                        self.answer.append(thisVertex)
                    self.answer.reverse()
                    findAnswer = False
                    break
            oldFront = newFront
            newFront = list()
            currentTime += 1

    def printAnswer(self):
        print [str(x) for x in self.answer]
        with open("ladder.out", "w") as file:
            file.write(self.srcWord + "\n")
            file.writelines("\n".join([str(x) for x in self.answer]))
            file.write("\n" + self.destWord)






def differentOneSymbol(first, second):
    if (len(first) is not len(second)):
        return False
    different = False
    for index in xrange(len(first)):
        if (first[index] is not second[index]):
            if (different is not False):
                return False
            different = True
    return different




def main():
    ladder = Ladder("ladder.in")
    ladder.buildGraph()
    ladder.searchChainOfWords()
    ladder.printAnswer()

if __name__ == '__main__':
    main()