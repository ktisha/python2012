# coding: utf-8

import ConfigParser
import time
import sys
import PIL.ImageTk as ImgTk
from Tkinter import *
import tkMessageBox
import life


class lifeGUI:
    def __init__(self, root, w, h, size, frames, initialState):

        self.canvasLocked = False
        self.globalLock = False
        self.stahp = False

        self.w = w
        self.h = h
        self.size = size
        self.rawField = initialState
        self.frames = frames
        self.field = life.field(self.rawField)
        
        self.root = root
        self.root.title = "Life"
        self.root.geometry(str(149 + w * size) + "x" + str(9 + h * size))

        self.clear = IntVar()
        self.currIter = StringVar()
        self.step = StringVar()

        self.backImg = ImgTk.PhotoImage(file = "prev.png")
        oneBackBtn = Button(self.root, command = self.moveOneBack, image = self.backImg)
        oneBackBtn.place(cnf = {"width": 32, "height": 32, "x": 3, "y": 3})

        currIterLbl = Label(self.root, textvariable = self.currIter)
        currIterLbl.place(cnf = {"width": 67, "height": 32, "x": 38, "y": 3})
        self.currIter.set("0")

        self.fwdImg = ImgTk.PhotoImage(file = "next.png")
        oneForwardBtn = Button(self.root, command = self.moveOneForward, image = self.fwdImg)
        oneForwardBtn.place(cnf = {"width": 32, "height": 32, "x": 108, "y": 3})

        self.manyBackImg = ImgTk.PhotoImage(file = "manyprev.png")
        manyBackBtn = Button(self.root, command = self.moveManyBack, image = self.manyBackImg)
        manyBackBtn.place(cnf = {"width": 32, "height": 32, "x": 3, "y": 38})

        stepEnt = Entry(self.root, textvariable = self.step)
        stepEnt.place(cnf = {"width": 67, "height": 30, "x": 38, "y": 39})
        stepEnt.focus()
        self.step.set("2")

        self.manyFwdImg = ImgTk.PhotoImage(file = "manynext.png")
        manyForwardBtn = Button(self.root, command = self.moveManyForward, image = self.manyFwdImg)
        manyForwardBtn.place(cnf = {"width": 32, "height": 32, "x": 108, "y": 38})

        stopBtn = Button(self.root, text = "Stahp", command = self.stop)
        stopBtn.place(cnf = {"width": 137, "height": 32, "x": 3, "y": 73})

        resetBtn = Button(self.root, text = "Reset", command = self.reset)
        resetBtn.place(cnf = {"width": 137, "height": 32, "x": 3, "y": 108})

        clearChk = Checkbutton(self.root, text = "Clear", variable = self.clear)
        clearChk.place(cnf = {"width": 128, "height": 32, "x": 3, "y": 143})

        self.canvas = Canvas(self.root, height = size * h + 1, width = size * w + 1, bg = "white")
        self.canvas.place(cnf={"x": 143, "y": 3})
        self.canvas.bind("<Button-1>", self.canvasClick)
        self.canvasDraw()

    def move(self, delta):
        if not self.canvasLocked:
            self.field = life.field(self.rawField)
        self.canvasLocked = True
        result = self.field.generate(self.field.getCurrIter() + delta)
        if result == "Field too big":
            tkMessageBox.showerror("", u"Слишком большое поле")
        elif result == "No prev":
            tkMessageBox.showinfo("", u"Нет предыдущего состояния")
        else:
            self.rawField = self.field.getField()
            self.canvasDraw()
            self.currIter.set(str(self.field.getCurrIter()))

    def moveOneBack(self):
        if self.globalLock:
            return
        self.move(-1)

    def moveOneForward(self):
        if self.globalLock:
            return
        self.move(1)

    def moveManyBack(self):
        if self.globalLock:
            return
        if not self.step.get().isdigit():
            return
        else:
            self.globalLock = True
            for i in xrange(0, -int(self.step.get()), -1):
                self.move(-1)
                self.root.update()
                time.sleep(0.1)
                if self.stahp:
                    self.stahp = False
                    break
            self.globalLock = False

    def moveManyForward(self):
        if self.globalLock:
            return
        if not self.step.get().isdigit():
            return
        else:
            self.globalLock = True
            for i in xrange(int(self.step.get())):
                self.move(1)
                self.root.update()
                time.sleep(0.1)
                if self.stahp:
                    self.stahp = False
                    break
            self.globalLock = False

    def stop(self):
        if self.globalLock:
            self.stahp = True

    def reset(self):
        if self.globalLock:
            return
        self.canvasLocked = False
        if self.clear.get() == 1:
            self.rawField = [list(x) for x in [[0]*self.w]*self.h]
        else:
            self.rawField = self.field.getField()
        self.currIter.set("0")
        self.canvasDraw()

    def canvasClick(self, event):
        if self.globalLock:
            return
        if self.canvasLocked:
            return
        else:
            x = int((event.x - 1) / self.size)
            y = int((event.y - 1) / self.size)
            self.rawField[y][x] = 1 - self.rawField[y][x]
            self.canvasDraw()

    def canvasDraw(self):
        self.canvas.delete("all")
        for i in xrange(w):
            for j in xrange(h):
                if self.frames:
                    self.canvas.create_rectangle(i * self.size + 2, j * self.size + 2, (i + 1) * self.size + 2, (j + 1) * self.size + 2, tags="all")
                    if self.rawField[j][i] == 1:
                        self.canvas.create_rectangle(i * self.size + 2 + 2, j * self.size + 2 + 2, (i + 1) * self.size - 2 + 2, (j + 1) * self.size - 2 + 2, fill="black", tags="all")
                else:
                    if self.rawField[j][i] == 1:
                        self.canvas.create_rectangle(i * self.size + 2, j * self.size + 2, (i + 1) * self.size + 2, (j + 1) * self.size + 2, fill="black", tags="all")

def readField(filename):
    strState = []
    with open(filename) as fieldFile:
        strState = [s.replace('\n', '') for s in fieldFile]
    h = len(strState)
    w = len(strState[0])
    initialState = [list(x) for x in [[0]*w]*h]
    for i in xrange(h):
        initialState[i] = [int(x) for x in strState[i]]
    return initialState

w, h, size, frames = 6, 6, 42, True
initialState = [list(x) for x in [[0]*w]*h]

if len(sys.argv) == 2:
    config = ConfigParser.ConfigParser()
    config.read(sys.argv[1])

    def getInt(str):
        if config.has_option("Config", str):
            return config.getint("Config", str)
        else:
            return eval(str)

    def getBool(str):
        if config.has_option("Config", str):
            return bool(config.getint("Config", str))
        else:
            return eval(str)

    def getStr(str):
        if config.has_option("Config", str):
            return config.get("Config", str)
        else:
            return eval(str)

    w = getInt("w")
    h = getInt("h")
    initialState = [list(x) for x in [[0]*w]*h]
    size = getInt("size")
    frames = getBool("frames")

    init = None
    init = getStr("init")
    if not (init is None):
        initialState = readField(init)
        h = len(initialState)
        w = len(initialState[0])

root = Tk()
lifeGUI(root, w, h, size, frames, initialState)
root.mainloop()