#!/usr/bin/python
#-*- coding: utf-8 -*-
__author__ = 'Anton M Alexeyev'

from Tkinter import *
import tkFont
from converter import *

# main frame construction
root = Tk()

#label fonts construction
labelFont = tkFont.Font(family = "Courier", size = 18)
radioFont = tkFont.Font(family = "Courier", size = 11)

# header label construction
static_string = StringVar()
headerLabel = Label(root, textvariable = static_string, relief = FLAT, font = labelFont)
static_string.set(u"Введите слово:")
headerLabel.pack()

#text field construction
textFont = tkFont.Font(family = "Courier", size = 16)
text = Text(root, height = 2, width = 20, font = textFont)
text.insert(END, "person")
text.pack()

var = StringVar()

def print_suggestions():
    input_text = text.get(1.0, END)
    collector = []
    string  = ""
    try:
        if rb_var.get() == 1:
            collector = get_euclidean_vector_by_token(7, get_token_by_word(input_text))
        if rb_var.get() == 2:
            collector = get_cosine_vector_by_token(7, get_token_by_word(input_text))
        if rb_var.get() == 3:
            collector = get_frequential_vector_by_token(7, get_token_by_word(input_text))
        collector = [element[1] for element in collector]
    except KeyError:
        string = u"Такого элемента нет!"
    for element in collector:
        string += element  + "\n"
    var.set(string)
    bottomLabel.pack()

# radiobuttons
rb_var = IntVar()

rb_eucl = Radiobutton(root, text = "Euclidean distance", variable = rb_var, value = 1, font = radioFont)
rb_cosine = Radiobutton(root, text = "Cosine  similarity", variable = rb_var, value = 2, font = radioFont)
rb_freq = Radiobutton(root, text = "Sorted   by   w[i]", variable = rb_var, value = 3, font = radioFont)
rb_eucl.select()

rb_eucl.pack()
rb_cosine.pack()
rb_freq.pack()

# button construction
B = Button(root, text = "Go!", command = print_suggestions,
    font = tkFont.Font(family = "Courier", size = 14))
B.pack()

# bottom header label construction
bhl_var = StringVar()
bhl_var.set(u"Термы:")
bottomHLabel = Label(root, textvariable = bhl_var, relief = FLAT, font = labelFont)
bottomHLabel.pack()

# bottom label construction
bottomLabel = Label(root, textvariable = var, relief = FLAT, font = labelFont)
bottomLabel.pack()

root.mainloop()