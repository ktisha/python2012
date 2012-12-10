__author__ = 'derketzer'

import SMART_ANT
import sys

def main():
    file_name = sys.argv[1]
    input_file = open(file_name, 'r')
    generationSize = 1000
    survivedSize = 100
    apples = 0
    s = input_file.readline()
    s = s.split(' ')
    mapSize = int(s[0])
    genomeSize = int(s[1])
    maxStep = int(s[2])
    torMap = [[0 for j in range(0, mapSize)] for i in range(0, mapSize)]
    for i in range(0, mapSize):
        s = input_file.readline()
        for j in range(0, mapSize):
            c = s[j]
            torMap[i][j] = 1 if (c == '*') else 0
            apples += torMap[i][j]
    input_file.close()
    smart_ant = SMART_ANT.SMART_ANT(generationSize, survivedSize, genomeSize, maxStep, mapSize, apples, torMap)
    st = smart_ant.makeMachine()
    print(file_name)
    print(st.genome.startState)
    act = ['M', 'R', 'L', 'N']
    for i in range(0, genomeSize):
        temp = st.genome.states[i]
        print(temp.outState0, temp.outState1, act[temp.actionToMove0], act[temp.actionToMove1])


if __name__=="__main__":
    main()