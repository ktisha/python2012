import sys
import queue
import time
import os
from PyQt4 import QtGui, QtCore, Qt


n = 0
m = 0
start = []
finish = []
wall =  list()
path = list()


class ColoredRect(QtGui.QGraphicsItem):
    def __init__(self, x1, y1, x2, y2, color):
        super(ColoredRect, self).__init__()
        self.rect = QtCore.QRectF(x1, y1, x2, y2)
        self.color = color
    
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setPen(0)
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(self.rect)


class MyView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.hardPen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        self.softPen = QtGui.QPen(QtCore.Qt.black, 0.25, QtCore.Qt.SolidLine)
        self.orange = QtGui.QColor(255, 165, 0)
        self.blue = QtGui.QColor(0, 191, 255)
        self.grid = list()
        self.walls = list()
        self.wallsAnim = list()


        self.frame = QtGui.QGraphicsRectItem(0, 0, n*20, m*20)
        self.start = ColoredRect(start[0]*20 - 19, start[1]*20 - 19, 19, 19, self.orange)
        self.finish = ColoredRect(finish[0]*20 - 19, finish[1]*20 - 19, 19, 19, self.blue)
        for i in range(n):
            self.grid += [QtGui.QGraphicsLineItem(20*i, 0, 20*i, 20*m)]
        for i in range(m):
            self.grid += [QtGui.QGraphicsLineItem(0, 20*i, 20*n, 20*i)]
        
        for w in wall:
            if w[0] == 0:
                self.walls = self.walls + [QtGui.QGraphicsLineItem(w[1]*20, w[2]*20 - 20, w[1]*20, w[2]*20)]
            else:
                self.walls = self.walls + [QtGui.QGraphicsLineItem(w[1]*20 - 20, w[2]*20, w[1]*20, w[2]*20)]
        self.walker = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('cross.bmp'))
        self.scene.addItem(self.walker)

        self.frame.setPen(self.hardPen)
        self.scene.addItem(self.frame)
        self.scene.addItem(self.start)
        self.scene.addItem(self.finish)
        for w in self.grid:
            w.setPen(self.softPen)
            self.scene.addItem(w)
        for w in self.walls:
            w.setPen(self.hardPen)
            self.scene.addItem(w)
        self.scene.setSceneRect(0, 0, n*20, m*20)
        self.scene.setFocusItem(self.walker)
        self.setScene(self.scene)

        l = len(path)
        if l == 0:
            self.d = QtGui.QMessageBox(self)
            self.d.setModal(True)
            self.d.setIcon(QtGui.QMessageBox.Information)
            self.d.setText('Path not found. Try another labyrinth or more bombs.')
            self.d.setWindowTitle('You shall not pass!')
            self.d.show()
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

        for i in range(l):
            self.a.setPosAt(i/l,  QtCore.QPointF(-20 + path[i][1]*20, -20 + path[i][2]*20))
            if i < l - 1:
                if path[i+1][0] > path[i][0]:
                    w = findwall(path[i][1], path[i][2], path[i+1][1], path[i+1][2])
                    j = wall.index(w)
                    self.wallsAnim[j].setPosAt(i/l, QtCore.QPointF(0,0))
                    self.wallsAnim[j].setRotationAt(i/l, 0)
                    self.wallsAnim[j].setRotationAt((i+1)/l, 720)
                    print(n - w[1], m - w[2])
                    self.wallsAnim[j].setPosAt((i+1)/l, QtCore.QPointF(20*(n - w[1]),20*(m - w[2])))
        self.tl.start()


class MainWindow(QtGui.QWidget):
    def __init__(self, par):
        super(MainWindow, self).__init__()
        self.parent = par
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, min(500, n*20 + 26), min(500, m*20 + 55))
        self.setWindowTitle('Aperture Laboratories')
        self.MV = MyView()
        self.bt = QtGui.QPushButton('Choose New Labyrinth')
        self.bt.clicked.connect(self.parent.startOver)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.MV)
        vbox.addWidget(self.bt)
        self.setLayout(vbox)
                  

def findwall(x0, y0, x1, y1):
        if abs(x0 - x1) + abs(y0 - y1) != 1:
            return -1
        if x0 - x1 != 0:
            return (0, min(x0, x1), y0)
        else:
            return (1, x0, min(y0, y1))
            

def prework(fname):
    if fname == '':
        return ''
    """ Input starts here """
    f = open(fname, "r")
    s = f.readline()
    global n
    global m
    n,m = s.split(" ")
    n = int(n)
    m = int(m)
    s = f.readline()
    x0,y0,x1,y1 = s.split(" ")
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    global start
    global finish
    start, finish = (x0, y0), (x1, y1)
    s = f.readline()
    k = int(s)
    s = f.readline()
    global wall
    wall = list()
    global path
    path = list()
    while(s):
        q,w,e = s.split(" ")
        q = int(q)
        w = int(w)
        e = int(e)
        wall = wall + [(q,w,e)]
        s = f.readline()
    f.close()
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
                    
    if d[(k, x1, y1)] == INFTY:
        path = []
        return
    for i in range(k):
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
    path = [cur]
    while not prev[cur] == cur:
        path = [prev[cur]] + path
        cur = prev[cur]

       

class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.connect(self, QtCore.SIGNAL('lastWindowClosed()'), self.exit)
        self.main = None
        self.startOver()
        
    def startOver(self):
        fname = QtGui.QFileDialog.getOpenFileName(None, 'Choose labyrinth file')
        if prework(fname) == '':
            return
        if not self.main == None:
            self.main.close()
        self.main = MainWindow(self)
        self.main.show()

    def noPath(self):
        self.dialog
        


def main():
    global app
    app = App(sys.argv)
    app.exec_()


if __name__ == '__main__':
    main()

