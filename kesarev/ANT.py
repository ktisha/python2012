__author__ = 'derketzer'
import GENOME

def sign(x):
    return 1 if(x >= 0) else -1

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
        map = [[mapSource[i][j] for j in range(0, len(mapSource[i]))] for i in range(0, len(mapSource))]
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

            if x >= mapSize or x < 0:
                x -= mapSize * sign(x)
            if y >= mapSize or y < 0:
                y -=  mapSize * sign(y)

            nextX = x
            nextY = y
            if rotation == 0:
                nextX += 1
            elif rotation == 1:
                nextY += 1
            elif rotation == 2:
                nextX -= 1
            elif rotation == 3:
                nextY -= 1

            if nextX >= mapSize or nextX < 0:
                nextX -= mapSize * sign(nextX)
            if nextY >= mapSize or nextY < 0:
                nextY -= mapSize * sign(nextY)

            action = st.getAction(map[nextY][nextX])
            outState = st.getOutState(map[nextY][nextX])
            st = self.genome.getState(outState)
            if action == 0:
                x = nextX
                y = nextY
                if map[nextY][nextX] == 1:
                    apples -= 1
                    map[nextY][nextX] = 0
                    if moves < maxStep:
                        self.applesWasEat += 1

            elif action == 2:
                rotation -= 1
                if rotation < 0:
                    rotation = 3
            elif action == 1:
                rotation += 1
                if rotation > 3:
                    rotation = 0
            elif action == 3:
                pass
            moves += 1
        self.moveToEatAllApples = moves
        self.prior = self.applesWasEat + (maxStep - self.moveToEatAllApples) / (float(maxStep))