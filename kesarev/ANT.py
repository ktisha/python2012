__author__ = 'derketzer'
import GENOME

def sign(x):
    return 1 if(x >= 0) else -1

def absolute_value(x):
    return x if(x >= 0) else -x

class ANT:
    def __init__(self, size, g = None):
        if g is None:
            self.genome = GENOME.GENOME(size)
        else:
            self.genome = g
        self.prior = -1
        self.applesWasEat = 0
        self.moveToEatAllApples = 0
        self.livingTime = 1

    def changePrior(self, p):
        self.prior = p

    def returnPriority(self):
        return self.prior

    def returnAppleNumber(self):
        return self.applesWasEat

    def makeMoves(self, maxStep, mapSize, appleNumber, mapSource):
        torMap = [[mapSource[i][j] for j in range(0, len(mapSource[i]))] for i in range(0, len(mapSource))]
        self.applesWasEat = 0
        self.moveToEatAllApples = 0
        self.livingTime += 1
        x = 0
        y = 0
        rotation = 0
        st = self.genome.getStartState()
        moves = 0
        apples = appleNumber
        while not apples == 0 and moves < 1.5 * maxStep:

            nextX = x
            nextY = y
            if absolute_value(rotation) == 1:
                nextY += sign(rotation)
            else:
                nextX += sign(rotation)

            if nextX >= mapSize or nextX < 0:
                nextX -= mapSize * sign(nextX)
            if nextY >= mapSize or nextY < 0:
                nextY -= mapSize * sign(nextY)

            action = st.getAction(torMap[nextY][nextX])
            outState = st.getOutState(torMap[nextY][nextX])
            st = self.genome.getState(outState)
            if action == 0:
                x = nextX
                y = nextY
                if torMap[y][x] == 1:
                    apples -= 1
                    torMap[y][x] = 0
                    if moves < maxStep:
                        self.applesWasEat += 1

            elif action == 2:
                rotation -= 1
                if rotation < -2:
                    rotation = 1
            elif action == 1:
                rotation += 1
                if rotation > 1:
                    rotation = -2
            moves += 1
        self.moveToEatAllApples = moves
        self.prior = self.applesWasEat + (maxStep - self.moveToEatAllApples) / (float(maxStep))