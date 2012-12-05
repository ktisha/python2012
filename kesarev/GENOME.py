__author__ = 'derketzer'
import STATE
import random

class GENOME:
    def __init__(self, size):
        self.genomeSize = size
        self.startState = random.randint(0, self.genomeSize - 1)
        self.states = []
        for i in range(0, self.genomeSize):
            out0 = random.randint(0, self.genomeSize - 1)
            out1 = random.randint(0, self.genomeSize - 1)
            action0 = random.randint(0, 3)
            action1 = random.randint(0, 3)
            self.states.append(STATE.STATE(out0, out1, action0, action1))

    def getState(self, i):
        return self.states[i]

    def getStartState(self):
        return self.states[self.startState]
