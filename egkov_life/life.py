from Tkinter import *

import random
import time

root = Tk()
root.title("GAMEofLIFE")

height = 50
width = 50
cell = 15
timeLimit = 0
ct = 0
flag = 0
initial = 1
timeScale = Scale (root)

field = [[[0 for wid in range (0, width + 2)] for hei in range(0, height + 2)] for time in range (0, 1)]
frameField = [[0 for wid in range (0, width)] for hei in range(0, height)]
colorField = [['black' for wid in range (0, width)] for hei in range(0, height)]

field[0][2][2] = 1
field[0][3][3] = 1
field[0][3][4] = 1
field[0][4][2] = 1
field[0][4][3] = 1

def extend (t) :

  global timeLimit
	global field

	if (t > timeLimit) :

		for time in range (timeLimit + 1, t + 1) :

			field.append ([[0 for wid in range (0, width + 2)] for hei in range(0, height + 2)])

			for i in range (1, height + 1) :
				for j in range (1, width + 1) :
					field[time][i][j] = nextValue (time - 1, i, j)

		timeLimit = t

	if (t <= timeLimit) :

		for i in range (1, height + 1) :
				for j in range (1, width + 1) :
					field[t][i][j] = nextValue (t - 1, i, j)

def nextValue (t, i, j):

    neighbours = 0

    if field[t][i-1][j-1] == 1:
    	neighbours = neighbours + 1
    if field[t][i-1][j] == 1:
    	neighbours = neighbours + 1
    if field[t][i-1][j+1] == 1:
    	neighbours = neighbours + 1
    if field[t][i][j-1] == 1:
    	neighbours = neighbours + 1
    if field[t][i][j+1] == 1:
    	neighbours = neighbours + 1
    if field[t][i+1][j-1] == 1:
    	neighbours = neighbours + 1
    if field[t][i+1][j] == 1:
    	neighbours = neighbours + 1
    if field[t][i+1][j+1] == 1:
    	neighbours = neighbours + 1

    if ((((neighbours < 2) or (neighbours > 3)) and (field[t][i][j] == 1)) or ((neighbours != 3) and (field[t][i][j] == 0))) :
    	return 0
    else:
    	return 1

def drawCell (i, j) :

	if ((1 <= i) and (i < height + 1) and (1 <= j) and (j < width + 1)) :

		if (flag == 0) :
			cNextValue = field [ct + 1][i][j]
		else :
			cNextValue = nextValue (ct, i, j)

		if (field[ct][i][j] == 0) :
			if (cNextValue == 0) :
				colorState = 'black'
			else :
				colorState = '#202020'
		else :
			if (cNextValue == 1) :
				colorState = 'white'
			else :
				colorState = '#EBEBEB'

		if (initial == 1) :
			if (frameField[i-1][j-1] == 0) :
				colorField[i-1][j-1] = colorState
				frameField[i-1][j-1] = Frame (root, bg = colorState, width = cell, height = cell, borderwidth = 1, relief = SUNKEN)
				frameField[i-1][j-1].grid (row = i, column = j)
				frameField[i-1][j-1].bind ("<Button-1>", lambda event, arg = [i, j] : callback (event, arg))

		else :
			if ((colorState != colorField[i-1][j-1]) or (frameField[i-1][j-1] == 0)) :
				colorField[i-1][j-1] = colorState
				frameField[i-1][j-1].configure (bg = colorState)

def callback (event, arg) :
	if (flag == 1) :
		i = arg[0]
		j = arg[1]
		if (field[ct][i][j] == 0) :
			field[ct][i][j] = 1
		else :
			field[ct][i][j] = 0
		print i
		print j
		drawCell (i - 1, j - 1)
		drawCell (i - 1, j)
		drawCell (i - 1, j + 1)
		drawCell (i, j - 1)
		drawCell (i, j)
		drawCell (i, j + 1)
		drawCell (i + 1, j - 1)
		drawCell (i + 1, j)
		drawCell (i + 1, j + 1)

def moveForward (event) :
	global ct
	ct = ct + 1
	extend (ct + 1)
	timeScale.configure (to = timeLimit)
	timeScale.set (ct)
	drawField ()

def moveBack (event) :
	global ct
	if (ct > 0) :
		ct = ct - 1
		extend (ct + 1)
		timeScale.configure (to = timeLimit)
		timeScale.set (ct)
		drawField ()

def moveTo (v) :
	global ct
	ct = timeScale.get ()
	extend (ct + 1)
	timeScale.configure (to = timeLimit)
	drawField ()

def change (event, arg) :
	global flag
	global changeField
	flag = 1
	arg.grid_remove ()
	changeField = Button (root, text = "Set")
	changeField.grid (row = height + 1, column = 1 + width / 2, columnspan = width / 2)
	changeField.bind ("<Button-1>", lambda event, arg = changeField : set (event, arg))

def set (event, arg) :
	global flag
	global changeField
	flag = 0
	extend (ct + 1)
	arg.grid_remove ()
	changeField = Button (root, text = "Change")
	changeField.grid (row = height + 1, column = 1 + width / 2, columnspan = width / 2)
	changeField.bind ("<Button-1>", lambda event, arg = changeField : change (event, arg))

def drawField () :
	global initial
	for i in range (1, height + 1) :
		for j in range (1, width + 1) :
			drawCell (i, j)
	initial = 0

timeScale.grid_remove ()
timeScale = Scale (root, from_= 0, to = timeLimit, length = cell * height)
timeScale.configure (variable = timeScale, tickinterval = 1, command = moveTo)
timeScale.configure (activebackground = 'white', showvalue = 0, sliderlength = 20)
timeScale.configure (troughcolor = 'black')
timeScale.grid (row = 1, rowspan = height + 1, column = width + 1)

next = Button (root, text = "->")
next.grid (row = height + 1, column = 1 + width / 3, columnspan = width / 3, sticky = W)
next.bind ("<Button-1>", moveForward)

prev = Button (root, text = "<-")
prev.grid (row = height + 1, column = 1, columnspan = width / 3, sticky = E)
prev.bind ("<Button-1>", moveBack)

changeField = Button (root, text = "Change")
changeField.grid (row = height + 1, column = 1 + 2 * width / 3, columnspan = width / 3)
changeField.bind ("<Button-1>", lambda event, arg = changeField : change (event, arg))

extend (1)
timeScale.configure (to = timeLimit)
drawField ()

root.mainloop()