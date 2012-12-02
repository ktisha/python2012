__author__ = 'derketzer'

import SMART_ANT

def main():
    file_name = "t6.txt"
    file = open(file_name, 'r', encoding='utf-8')
    generationSize = 1000
    survivedSize = 100
    apples = 0
    s = file.readline()
    s = s.split(' ')
    mapSize = int(s[0])
    genomeSize = int(s[1])
    maxStep = int(s[2])
    map = [[0 for j in range(0, mapSize)] for i in range(0, mapSize)]
    for i in range(0, mapSize):
        s = file.readline()
        for j in range(0, mapSize):
            c = s[j]
            map[i][j] = 1 if (c == '*') else 0
            apples += map[i][j]

    smart_ant = SMART_ANT.SMART_ANT(generationSize, survivedSize, genomeSize, maxStep, mapSize, apples, map)
    st = smart_ant.makeMachine()
    print(file_name)
    print(st.genome.startState)
    act = ['M', 'R', 'L', 'N']
    for i in range(0, genomeSize):
        temp = st.genome.states[i]
        print(temp.outState0, temp.outState1, act[temp.actionToMove0], act[temp.actionToMove1])


if __name__=="__main__":
    main()