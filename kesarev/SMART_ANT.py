__author__ = 'derketzer'
import ANT
import random
import STATE

class SMART_ANT:
    def __init__(self, generationSize, survived, genomeSize, maxStep, mapSize, apples, tMap):
        random.seed(None)
        self.generationSize = generationSize
        self.genomeSize = genomeSize
        self.generation = []
        self.antsToLove = []
        self.maxStepToAnt = maxStep
        self.sizeOfMap = mapSize
        self.appleNumber = apples
        self.torMap = tMap
        self.survivedAnts = survived
        self.generationNumber = 0

    def makeMachine(self):
        self.makeFirstGeneration()
        self.generationNumber = 1
        lastResult = 0
        generationToLittleShake = 200
        generationToBigShake = 1000
        while self.generation[0].returnAppleNumber() != self.appleNumber:
            if not lastResult == self.generation[0].returnAppleNumber():
                generationToLittleShake = 200
                generationToBigShake = 1000
                lastResult = self.generation[0].returnAppleNumber()
            if generationToLittleShake == 0 and generationToBigShake != 0:
                generationToLittleShake = 200
                self.makeLittleShake()
            if generationToBigShake == 0:
                generationToLittleShake = 200
                generationToBigShake = 1000
                self.makeBigShake()
            self.makeNextGeneration()
            print("#", self.generationNumber, ", apples was eat: ", self.generation[0].returnAppleNumber(),
                  "(", self.appleNumber, ")", generationToLittleShake, " ", generationToBigShake, " ")
            self.generationNumber += 1
            generationToLittleShake -= 1
            generationToBigShake -= 1
        return self.generation[0]

    def makeLittleShake(self):
        gs = int(len(self.generation) / 10)
        for i in range(gs, len(self.generation)):
            self.generation[i] =  ANT.ANT(self.genomeSize)
        print("Little Shake!\n")

    def makeBigShake(self):
        for i in range(0, len(self.generation)):
            self.generation[i] = ANT.ANT(self.genomeSize)
        print("BIG SHAKE!\n")

    def makeMutation(self, a):
        i = random.randint(0, self.genomeSize - 1)
        ant = self.generation[a]
        st = ant.genome.states[i]
        j = random.randint(0, 5)
        if j == 0:
            ant.genome.startState = random.randint(0, self.genomeSize - 1)
        elif j == 1:
            st.actionToMove0 = random.randint(0, 3)
        elif j == 2:
            st.actionToMove1 = random.randint(0, 3)
        elif j == 3:
            st.outState0 = random.randint(0, self.genomeSize - 1)
        elif j == 4:
            st.outState1 = random.randint(0, self.genomeSize - 1)
        elif j == 5:
            tempOut = st.outState0
            tempAction = st.actionToMove0
            st.outState0 = st.outState1
            st.outState1 = tempOut
            st.actionToMove0 = st.actionToMove1
            st.actionToMove1 = tempAction

    def makeLove(self, p1, p2):
        parent1 = self.generation[p1]
        parent2 = self.generation[p2]
        child1 = ANT.ANT(self.genomeSize)
        child2 = ANT.ANT(self.genomeSize)
        if random.randint(0, 1) == 1:
            child1.genome.startState = parent1.genome.startState
            child2.genome.startState = parent2.genome.startState
        else:
            child2.genome.startState = parent1.genome.startState
            child1.genome.startState = parent2.genome.startState
        for i in range(0, self.genomeSize):
            st1 = None
            st2 = None
            pst1 = parent1.genome.states[i]
            pst2 = parent2.genome.states[i]
            j = random.randint(0, 3)
            if j == 0:
                st1 = STATE.STATE(pst1.outState0, pst2.outState1, pst1.actionToMove0, pst2.actionToMove1)
                st2 = STATE.STATE(pst2.outState0, pst1.outState1, pst2.actionToMove0, pst1.actionToMove1)
            elif j == 1:
                st1 = STATE.STATE(pst2.outState0, pst1.outState1, pst2.actionToMove0, pst1.actionToMove1)
                st2 = STATE.STATE(pst1.outState0, pst2.outState1, pst1.actionToMove0, pst2.actionToMove1)
            elif j == 2:
                st1 = STATE.STATE(pst1.outState0, pst1.outState1, pst1.actionToMove0, pst1.actionToMove1)
                st2 = STATE.STATE(pst2.outState0, pst2.outState1, pst2.actionToMove0, pst2.actionToMove1)
            elif j == 3:
                st1 = STATE.STATE(pst2.outState0, pst2.outState1, pst2.actionToMove0, pst2.actionToMove1)
                st2 = STATE.STATE(pst1.outState0, pst1.outState1, pst1.actionToMove0, pst1.actionToMove1)
            child1.genome.states[i] = st1
            child2.genome.states[i] = st2
        self.generation.append(child1)
        self.generation.append(child2)

    def makeFirstGeneration(self):
        for i in range(0, self.survivedAnts):
            self.generation.append(ANT.ANT(self.genomeSize))

    def makeNextGeneration(self):
        while len(self.generation) < self.generationSize:
            i = random.randint(0, self.survivedAnts - 1)
            j = random.randint(0, self.survivedAnts - 1)
            if i == j:
                continue
            self.makeLove(i, j)
        for i in range(0, len(self.generation)):
            if random.randint(0, int(1000 / self.generation[i].livingTime) - 1) == 0:
                self.makeMutation(i)
                self.generation[i].livingTime = 0
        for i in range(0, len(self.generation)):
            self.generation[i].makeMoves(self.maxStepToAnt, self.sizeOfMap, self.appleNumber, self.torMap)
        self.generation.sort(key = lambda ant: ant.returnPriority(), reverse = True)
        while len(self.generation) > self.survivedAnts:
            self.generation.pop()

