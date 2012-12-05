# coding: utf-8

import math
import time

class field:

    def __init__(self, startpos):
        self.__h = len(startpos)
        self.__w = len(startpos[0])
        self.__startpos = startpos
        self.__currIter = 0
        self.__cache = {}
        self.__cache[0] = startpos
        self.__transitions = {}
        self.__fillTransitions()
    
    def __fillTransitions(self):
        try:
            with open("dict", 'r') as f:
                for i in xrange(0, 2 ** 16):
                    s = f.readline().replace('\n', '')
                    s = [int(a) for a in s.split(' ')]
                    self.__transitions[i] = ((s[0], s[1]),
                                             (s[2], s[3]))
        except:
            with open("dict", 'w') as f:
                getBit = lambda value, number: (value >> number) % 2
                def check(cell, neib):
                    if cell == 0:
                        if neib == 3:
                            return 1
                        else:
                            return  0
                    else:
                        if 2 <= neib <= 3:
                            return 1
                        else:
                            return 0

                for i in xrange(0, 2 ** 16):
                    index = (((getBit(i, 0 )), (getBit(i, 1 )), (getBit(i, 2 )), (getBit(i, 3 ))),
                             ((getBit(i, 4 )), (getBit(i, 5 )), (getBit(i, 6 )), (getBit(i, 7 ))),
                             ((getBit(i, 8 )), (getBit(i, 9 )), (getBit(i, 10)), (getBit(i, 11))),
                             ((getBit(i, 12)), (getBit(i, 13)), (getBit(i, 14)), (getBit(i, 15))))
        
                    lt = index[1][1]
                    ltNeib = index[0][0] + index[0][1] + index[0][2] + \
                             index[1][0] +               index[1][2] + \
                             index[2][0] + index[2][1] + index[2][2]
                    lt = check(lt, ltNeib)
        
                    rt = index[1][2]
                    rtNeib = index[0][1] + index[0][2] + index[0][3] +\
                             index[1][1] +               index[1][3] +\
                             index[2][1] + index[2][2] + index[2][3]
                    rt = check(rt, rtNeib)
        
                    lb = index[2][1]
                    lbNeib = index[1][0] + index[1][1] + index[1][2] +\
                             index[2][0] +               index[2][2] +\
                             index[3][0] + index[3][1] + index[3][2]
                    lb = check(lb, lbNeib)
        
                    rb = index[2][2]
                    rbNeib = index[1][1] + index[1][2] + index[1][3] +\
                             index[2][1] +               index[2][3] +\
                             index[3][1] + index[3][2] + index[3][3]
                    rb = check(rb, rbNeib)
        
                    self.__transitions[i] = ((lt, rt),
                                             (lb, rb))
                    f.write("%i %i %i %i\n" % (lt, rt, lb, rb))

    def __generateUnhashed(self, num):

        # start = time.clock()

        if num < 0:
            raise ValueError

        bestKey = 0

        for key in self.__cache.keys():
            if key > bestKey:
                bestKey = key
            else:
                break

        curr = self.__cache[bestKey]

        get = lambda i, j: curr[i % self.__h][j % self.__w]

        def getNum(index):
            res = 0
            for i in xrange(0, 16):
                res += index[int(math.floor(i / 4))][i % 4] << i
            return res

        def check(cell, neib):
            if cell == 0:
                if neib == 3:
                    return 1
                else:
                    return  0
            else:
                if 2 <= neib <= 3:
                    return 1
                else:
                    return 0

        for step in xrange(bestKey, num):
            if step % 100 == 0:
                print step
            dest = [[]] * self.__h
            for i in xrange(0, self.__h):
                dest [i] = [0] * self.__w

            for i in xrange(0, self.__h):
                for j in xrange(0, self.__w):
                    neib = get(i-1, j-1) + get(i-1, j  ) + get(i-1, j+1) +\
                           get(i  , j-1) +                 get(i  , j+1) +\
                           get(i+1, j-1) + get(i+1, j  ) + get(i+1, j+1)
                    dest[i][j] = check(get(i, j), neib)
            curr = dest
            self.__cache[step] = curr

        # print "Unhashed: %f" % (time.clock() - start)
        return curr

    def __generate(self, num):
        # start = time.clock()
        if num < 0:
            raise ValueError

        bestKey = 0

        for key in self.__cache.keys():
            if key > bestKey:
                bestKey = key
            else:
                break

        curr = self.__cache[bestKey]

        get = lambda i, j: curr[i % self.__h][j % self.__w]

        def getNum(index):
            res = 0
            for i in xrange(0, 16):
                res += index[int(math.floor(i / 4))][i % 4] << i
            return res

        for step in xrange(bestKey, num):
            dest = [[]] * self.__h
            for i in xrange(0, self.__h):
                dest [i] = [0] * self.__w

            for i in xrange(0, self.__h, 2):
                for j in xrange(0, self.__w, 2):
                    index = getNum(((get(i-1, j-1), get(i-1, j  ), get(i-1, j+1), get(i-1, j+2)),
                                    (get(i  , j-1), get(i  , j  ), get(i  , j+1), get(i  , j+2)),
                                    (get(i+1, j-1), get(i+1, j  ), get(i+1, j+1), get(i+1, j+2)),
                                    (get(i+2, j-1), get(i+2, j  ), get(i+2, j+1), get(i+2, j+2))))
                    dest[(i  ) % self.__h][(j  ) % self.__w] = self.__transitions[index][0][0]
                    dest[(i  ) % self.__h][(j+1) % self.__w] = self.__transitions[index][0][1]
                    dest[(i+1) % self.__h][(j  ) % self.__w] = self.__transitions[index][1][0]
                    dest[(i+1) % self.__h][(j+1) % self.__w] = self.__transitions[index][1][1]
            curr = dest

        # print "Hashed: %f" % (time.clock() - start)
        return curr


    def move(self, delta):
        self.__currIter += delta
        if self.__currIter < 0:
            self.__currIter = 0

        self.__cache[self.__currIter] = self.__generateUnhashed(self.__currIter)
       #  self.__fillCache()

    def __fillCache(self):
        base = int(math.floor(self.__currIter / 10)) * 10 - 10         # Нижняя граница тридцатки, в которой находится текущий индекс
        indexes = []
        for i in xrange(10, 20):
            indexes.append(base + i)
        for power in xrange(0, 3):
            step = 30 ** power
            for i in xrange(-1, -11, -1):
                indexes.append(base + i * step)
            for i in xrange(1, 11, 1):
                indexes.append(base + step + i * step)
            base -= step

        indexes = filter(lambda i: i > 0, indexes)
        indexes.append(0)

        for key in self.__cache.keys():
            if not (key in indexes):
                self.__cache.pop(key)
        for index in indexes:
            if not self.__cache.has_key(index):
                print "cache miss: %i" % index
                # self.__cache[index] = self.__generate(index)
                self.__cache[index] = self.__generateUnhashed(index)

    def getField(self):
        return self.__cache[self.__currIter]

    def getCurrIter(self):
        return self.__currIter


def show(field):
    print field.getCurrIter()
    data = field.getField()
    print '----------'
    for row in data:
        s = str(row).replace(', ', '').replace('1', 'O').replace('0', ' ')[1:-1]
        print s
    print '----------'

start = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

#start = [[0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0],
#         [1, 1, 1, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0]]
f = field(start)
show(f)
while True:
    raw_input()
    f.move(100000)
    show(f)