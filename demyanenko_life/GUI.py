# coding: utf-8

import PIL.Image as Img
import PIL.ImageTk as ImgTk
from Tkinter import *
import tkMessageBox
import life


class lifeGUI:
    def __init__(self, root):

        self.canvasLocked = False
        self.rawField = [[0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0],
                         [0, 1, 1, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0]]

        self.field = life.field(self.rawField)

        root.title = "Life"
        root.geometry("401x261")

        self.clear = IntVar()
        self.currIter = StringVar()
        self.step = StringVar()

        self.backImg = ImgTk.PhotoImage(file="prev.png")
        oneBackBtn = Button(root, command=self.moveOneBack, image=self.backImg)
        oneBackBtn.place(cnf={"width": 32, "height": 32, "x": 3, "y": 3})

        currIterLbl = Label(root, textvariable=self.currIter)
        currIterLbl.place(cnf={"width": 67, "height": 32, "x": 38, "y": 3})
        self.currIter.set("0")

        self.fwdImg = ImgTk.PhotoImage(file="next.png")
        oneForwardBtn = Button(root, command=self.moveOneForward, image=self.fwdImg)
        oneForwardBtn.place(cnf={"width": 32, "height": 32, "x": 108, "y": 3})

        self.manyBackImg = ImgTk.PhotoImage(file="manyprev.png")
        manyBackBtn = Button(root, command=self.moveManyBack, image=self.manyBackImg)
        manyBackBtn.place(cnf={"width": 32, "height": 32, "x": 3, "y": 38})

        stepEnt = Entry(root, textvariable=self.step)
        stepEnt.place(cnf={"width": 67, "height": 30, "x": 38, "y": 39})
        stepEnt.focus()
        self.step.set("2")

        self.manyFwdImg = ImgTk.PhotoImage(file="manynext.png")
        manyForwardBtn = Button(root, command = self.moveManyForward, image=self.manyFwdImg)
        manyForwardBtn.place(cnf={"width": 32, "height": 32, "x": 108, "y": 38})

        resetBtn = Button(root, text="Reset", command = self.reset)
        resetBtn.place(cnf={"width": 137, "height": 32, "x": 3, "y": 73})

        clearChk = Checkbutton(root, text="Clear", variable=self.clear)
        clearChk.place(cnf={"width": 128, "height": 32, "x": 3, "y": 113})

        self.canvas = Canvas(root, height=252, width=252, bg="white")
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
        self.move(-1)

    def moveOneForward(self):
        self.move(1)

    def moveManyBack(self):
        if not self.step.get().isdigit():
            return
        else:
            self.move(-int(self.step.get()))

    def moveManyForward(self):
        if not self.step.get().isdigit():
            return
        else:
            self.move(int(self.step.get()))

    def reset(self):
        self.canvasLocked = False
        if self.clear.get() == 1:
            self.rawField =[list(x) for x in [[0]*6]*6]
        else:
            self.rawField = self.field.getField()
        self.currIter.set("0")
        self.canvasDraw()

    def canvasClick(self, event):
        if self.canvasLocked:
            return
        else:
            x = int(event.x / 42)
            y = int(event.y / 42)
            self.rawField[y][x] = 1 - self.rawField[y][x]
            self.canvasDraw()

    def canvasDraw(self):
        self.canvas.delete("all")
        for i in xrange(6):
            for j in xrange(6):
                self.canvas.create_rectangle(i * 42, j * 42, i * 42 + 42, j * 42 + 42, tags="all")
                if self.rawField[j][i] == 1:
                    self.canvas.create_rectangle(i * 42 + 2, j * 42 + 2, i * 42 + 40, j * 42 + 40, fill="black", tags="all")

root = Tk()
lifeGUI(root)
root.mainloop()