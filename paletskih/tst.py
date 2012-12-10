import sys
import queue
import time
from PyQt4 import QtGui, QtCore

f = open("input1.txt", "r")
s = f.readline()
n,m = s.split(" ")
n = int(n)
m = int(m)
s = f.readline()
x0,y0,x1,y1 = s.split(" ")
x0 = int(x0)
y0 = int(y0)
x1 = int(x1)
y1 = int(y1)
s = f.readline()
k = int(s)
s = f.readline()
wall = list()
path = list()
while(s):
    q,w,e = s.split(" ")
    q = int(q)
    w = int(w)
    e = int(e)
    wall = wall + [(q,w,e)]
    s = f.readline()

""" We do believe input is correct"""



class MyView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.hardPen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        self.softPen = QtGui.QPen(QtCore.Qt.black, 0.25, QtCore.Qt.SolidLine)
        self.frame = list()
        self.grid = list()
        self.walls = list()
        self.wallsAnim = list()

        self.frame += [QtGui.QGraphicsLineItem(0, 0, 20*n, 0)]
        self.frame += [QtGui.QGraphicsLineItem(0, 0, 0, 20 * m)]
        self.frame += [QtGui.QGraphicsLineItem(20*n, 0, 20*n, 20*m)]
        self.frame += [QtGui.QGraphicsLineItem(0, 20*m, 20*n, 20*m)]
        for i in range(n):
            self.grid += [QtGui.QGraphicsLineItem(20*i, 0, 20*i, 20*m)]
        for i in range(m):
            self.grid += [QtGui.QGraphicsLineItem(0, 20*i, 20*n, 20*i)]
        
        for w in wall:
            if w[0] == 0:
                self.walls = self.walls + [QtGui.QGraphicsLineItem(w[1]*20, w[2]*20 - 20, w[1]*20, w[2]*20)]
            else:
                self.walls = self.walls + [QtGui.QGraphicsLineItem(w[1]*20 - 20, w[2]*20, w[1]*20, w[2]*20)]
        self.walker = QtGui.QGraphicsPixmapItem(QtGui.QPixmap("cross.bmp"))
        self.scene.addItem(self.walker)

        for w in self.frame:
            w.setPen(self.hardPen)
            self.scene.addItem(w)
        for w in self.grid:
            w.setPen(self.softPen)
            self.scene.addItem(w)
        for w in self.walls:
            w.setPen(self.hardPen)
            self.scene.addItem(w)
        self.setScene(self.scene)

        # Remember to hold the references to QTimeLine and QGraphicsItemAnimation instances.
        # They are not kept anywhere, even if you invoke QTimeLine.start()
        l = len(path)
        self.tl = QtCore.QTimeLine(1000 * l)
        self.tl.setFrameRange(0, l * 100)
        for w in self.walls:
            a = QtGui.QGraphicsItemAnimation()
            a.setItem(w)
            a.setTimeLine(self.tl)
            self.wallsAnim += [a]
        self.a = QtGui.QGraphicsItemAnimation()
        self.a.setItem(self.walker)
        self.a.setTimeLine(self.tl)

        # Each method determining an animation state (e.g. setPosAt, setRotationAt etc.)
        # takes as a first argument a step which is a value between 0 (the beginning of the
        # animation) and 1 (the end of the animation)
        for i in range(l):
            self.a.setPosAt(i/l,  QtCore.QPointF(-15 + path[i][1]*20, -15 + path[i][2]*20))
            if i < l - 1:
                if path[i+1][0] > path[i][0]:
                    w = findwall(path[i][1], path[i][2], path[i+1][1], path[i+1][2])
                    j = wall.index(w)
                    self.wallsAnim[j].setPosAt(i/l, self.wallsAnim[j].posAt(0))
                    self.wallsAnim[j].setRotationAt(i/l, 0)
                    self.wallsAnim[j].setRotationAt((i+1)/l, 360)
                    self.wallsAnim[j].setPosAt((i+1)/l, QtCore.QPointF(210,170))
        self.tl.start()

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 315, 315)
        self.setWindowTitle('Aperture Laboratories')
        self.MV = MyView()
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.MV)
        self.bt = QtGui.QPushButton("Retry")
        self.bt.clicked.connect(self.restart)
        self.vbox.addWidget(self.bt)
        self.setLayout(self.vbox)
        self.show()

    def restart(self):
        pass
        

def findwall(x0, y0, x1, y1):
        if abs(x0 - x1) + abs(y0 - y1) != 1:
            return -1
        if x0 - x1 != 0:
            return (0, min(x0, x1), y0)
        else:
            return (1, x0, min(y0, y1))
            

def main():
    """Bfs and pre-calc starts here"""
    INFTY = 999999
    d = dict()
    prev = dict()
    i = 1
    j = 1
    l = 0
    while i <= n:
        j = 1
        while j <= m:
            l = 0
            while l <= k:
                d[(l,i,j)] = INFTY
                l = l + 1
            j = j + 1
        i = i + 1
    d[(0,x0,y0)] = 0
    prev[(0,x0,y0)] = (0,x0,y0)
    q = queue.Queue()
    q.put((0,x0,y0))
    while (not q.empty()):
        cur = q.get()
        dist = d[cur]
        
        if (cur[2] < m):
            if (not (1,cur[1],cur[2]) in wall):
                if d[(cur[0], cur[1], cur[2] + 1)] > dist + 1:
                    d[(cur[0], cur[1], cur[2] + 1)] = dist + 1
                    prev[(cur[0], cur[1], cur[2] + 1)] = cur
                    q.put((cur[0],cur[1],cur[2] + 1))
            else:
                if (cur[0] < k and d[(cur[0] + 1, cur[1], cur[2] + 1)]) > dist + 1:
                    d[(cur[0] + 1, cur[1], cur[2] + 1)] = dist + 1
                    prev[(cur[0] + 1, cur[1], cur[2] + 1)] = cur
                    q.put((cur[0] + 1,cur[1],cur[2] + 1))
            
        if (cur[2] > 1):
            if (not (1,cur[1],cur[2] - 1) in wall):
                if d[(cur[0], cur[1], cur[2] - 1)] > dist + 1:
                    d[(cur[0], cur[1], cur[2] - 1)] = dist + 1
                    prev[(cur[0], cur[1], cur[2] - 1)] = cur
                    q.put((cur[0],cur[1],cur[2] - 1))
            else:
                if (cur[0] < k and d[(cur[0] + 1, cur[1], cur[2] - 1)]) > dist + 1:
                    d[(cur[0] + 1, cur[1], cur[2] - 1)] = dist + 1
                    prev[(cur[0] + 1, cur[1], cur[2] - 1)] = cur
                    q.put((cur[0] + 1,cur[1],cur[2] - 1))
        
        if (cur[1] < n):
            if (not (0,cur[1],cur[2]) in wall):
                if d[(cur[0], cur[1] + 1, cur[2])] > dist + 1:
                    d[(cur[0], cur[1] + 1, cur[2])] = dist + 1
                    prev[(cur[0], cur[1] + 1, cur[2])] = cur
                    q.put((cur[0],cur[1] + 1,cur[2]))
            else:
                if (cur[0] < k and d[(cur[0] + 1, cur[1] + 1, cur[2])]) > dist + 1:
                    d[(cur[0] + 1, cur[1] + 1, cur[2])] = dist + 1
                    prev[(cur[0] + 1, cur[1] + 1, cur[2])] = cur
                    q.put((cur[0] + 1,cur[1] + 1,cur[2]))

        if (cur[1] > 1):
            if (not (0,cur[1] - 1,cur[2]) in wall):
                if d[(cur[0], cur[1] - 1, cur[2])] > dist + 1:
                    d[(cur[0], cur[1] - 1, cur[2])] = dist + 1
                    prev[(cur[0], cur[1] - 1, cur[2])] = cur
                    q.put((cur[0],cur[1] - 1,cur[2]))
            else:
                if (cur[0] < k and d[(cur[0] + 1, cur[1] - 1, cur[2])]) > dist + 1:
                    d[(cur[0] + 1, cur[1] - 1, cur[2])] = dist + 1
                    prev[(cur[0] + 1, cur[1] - 1, cur[2])] = cur
                    q.put((cur[0] + 1,cur[1] - 1,cur[2]))
                    

    i = 0
    while i <= k:
        print (d[(i,x1,y1)])
        i = i + 1
    i = 0
    j = 0
    while i <= k:
        if (d[(i,x1,y1)] < d[(j,x1,y1)]):
            j = i
        i = i + 1
    print (d[(j,x1,y1)])
    cur = (j, x1, y1)
    global path
    path = [cur]
    while not prev[cur] == cur:
        path = [prev[cur]] + path
        cur = prev[cur] 
    """And ends here"""
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
f.close()
