#!/usr/bin/python
#-*- coding: utf-8 -*-
__author__ = 'Anton M Alexeyev'

from Tkinter import *
import tkFont
from converter import *
import tkMessageBox
import tkFileDialog

# global variables i don't want the user to modify
closest_tokens_number = 8

# main frame construction
root = Tk()
root.title("HAL demo")
root.resizable(0, 0)
widgets_list = []

#label fonts construction
labelFont = tkFont.Font(family = "Courier", size = 18)
radioFont = tkFont.Font(family = "Courier", size = 11)

# header label construction
static_string = StringVar()
headerLabel = Label(root, textvariable = static_string, relief = FLAT, font = labelFont)
static_string.set(u"Enter the word:")
widgets_list += [headerLabel]

#text field construction
textFont = tkFont.Font(family = "Courier", size = 16)
text = Text(root, height = 2, width = 20, font = textFont)
text.insert(END, "person")
widgets_list += [text]

var = StringVar()

def print_suggestions():
    input_text = text.get(1.0, END)
    collector = []
    string  = ""
    try:
        if rb_var.get() == 1:
            collector = get_euclidean_vector_by_token(closest_tokens_number, get_token_by_word(input_text))
        if rb_var.get() == 2:
            collector = get_cosine_vector_by_token(closest_tokens_number, get_token_by_word(input_text))
        if rb_var.get() == 3:
            collector = get_frequential_vector_by_token(closest_tokens_number, get_token_by_word(input_text))
        if rb_var.get() == 4:
            collector = get_manhattan_vector_by_token(closest_tokens_number, get_token_by_word(input_text))
        collector = [element[1] for element in collector]
    except KeyError:
        string = u"No such element!"
    for element in collector:
        string += element  + "\n"
    var.set(string)
    global widgets_list
    widgets_list += [bottomLabel]

# radiobuttons
rb_var = IntVar()

rb_eucl = Radiobutton(root, text = "Euclidean distance", variable = rb_var, value = 1, font = radioFont)
rb_manh = Radiobutton(root, text = "Manhattan distance", variable = rb_var, value = 4, font = radioFont)
rb_cosine = Radiobutton(root, text = "Cosine  similarity", variable = rb_var, value = 2, font = radioFont)
rb_freq = Radiobutton(root, text = "Sorted   by   w[i]", variable = rb_var, value = 3, font = radioFont)
rb_eucl.select()

widgets_list += [rb_eucl, rb_manh, rb_cosine, rb_freq]

# button construction
go_button = Button(root, text = "Go!", command = print_suggestions,
    font = tkFont.Font(family = "Courier", size = 14))

widgets_list += [go_button]

# bottom header label construction
bhl_var = StringVar()
bhl_var.set(u"Terms:")
bottomHLabel = Label(root, textvariable = bhl_var, relief = FLAT, font = labelFont)
line = Frame(bg = "black", height = 1, width = 100)
widgets_list += [bottomHLabel, line]

# bottom label construction
bottomLabel = Label(root, textvariable = var, relief = FLAT, font = labelFont)
widgets_list += [bottomLabel]

#------------training section--------------

trainer = Frame()
trainer.pack()
intro_var = StringVar()
intro_var.set(u"Choose the corpus:")
Label(trainer, textvariable = intro_var, relief = FLAT, font = labelFont).pack()

# training model
def loadfile():
    filename = tkFileDialog.askopenfilename(filetypes = (("Text files", "*.txt"),
                                                         ("All files", "*.*") ))
    if filename:
        try:
            train_model(filename)
            tkMessageBox.showinfo("Notification", "Training done.")
            global widgets_list
            for widget in widgets_list:
                widget.pack()
        except Exception,e:
            tkMessageBox.showerror("Error", str(e))
            return

Button(trainer, text = u"Train", command = loadfile, width = 10).pack()

root.mainloop()