#coding: utf-8

from pop3 import *
import Tkinter
import ttk
import tkMessageBox
import argparse
import re

import logging
logging.basicConfig(level = logging.INFO)
font = 'Helvetica 12'


class GUI(Tk):

	def __init__(self, title):
		Tk.__init__(self)	
		self.wm_title(title)		

		dim = self.dimensions = dict()
		dim['width'] = 800
		dim['height'] = 400		
		self.minsize(dim['width'], dim['height'])
		self.maxsize(dim['width'], dim['height'])		

		dim['gap_x'] = dim['gap_y'] = 10
		dim['list_panel'] = 300

		self.createWidgets()
		self.showMessagesList()	
	
	def createWidgets(self):
		dim = self.dimensions

		list_panel_frame = Frame(self, width = dim['list_panel'])		
		self.msg_text_frame = LabelFrame(self, text = 'From:', font = font)

		list_panel_frame.place(x = 0, y = 0, width = dim['list_panel'], height = dim['height'])
		self.msg_text_frame.place(x = dim['list_panel'], y = 0, width = dim['width'] - dim['list_panel'], height = dim['height'])
		
		self.textbox = Text(self.msg_text_frame, font = font, wrap = 'word', state = 'disabled')
		text_scrollbar = Scrollbar(self.msg_text_frame)

		self.listbox = Listbox(list_panel_frame, font = font)		
		list_scrollbar = Scrollbar(list_panel_frame)
		self.listbox.bind('<<ListboxSelect>>', self.onSelect)

		text_scrollbar['command'] = self.textbox.yview
		self.textbox['yscrollcommand'] = text_scrollbar.set
		self.textbox.pack(side = 'left', fill = 'both', expand = 1)
		text_scrollbar.pack(side = 'right', fill = 'y')		

		list_scrollbar['command'] = self.listbox.yview
		self.listbox['yscrollcommand'] = list_scrollbar.set
		self.listbox.pack(side = 'left', fill = 'both', expand = 1)
		list_scrollbar.pack(side = 'right', fill = 'y')		

	def cache(self, msg_id, msg, sender):
		self.cached[msg_id] = msg	
		self.cached_senders[msg_id]	= sender

	def showMessagesList(self, n = 20):
		self.list_top_n = min(pop3.getMessageNumber(), n)
		self.cached = [None] * (self.list_top_n + 1)
		self.cached_senders = [None] * (self.list_top_n + 1)
		for i in xrange(self.list_top_n):
			meta, header = pop3.recieveHeader(self.list_top_n - i)
			self.listbox.insert(END, meta['subject'])

	def showMessage(self, msg_id):
		self.textbox['state'] = 'normal'	
		self.textbox.delete('1.0', 'end')
		if self.cached[msg_id]:
			msg = self.cached[msg_id]
		else:
			meta, msg = pop3.recieveMessageText(msg_id)
			self.cache(msg_id, msg, meta['from'])	
		self.textbox.insert('1.0', msg)
		self.textbox['state'] = 'disabled'

	def onSelect(self, evt):
		listbox = evt.widget
		index = int(listbox.curselection()[0])
		self.showMessage(self.list_top_n - index)
		self.msg_text_frame['text'] = 'From: ' + self.cached_senders[self.list_top_n - index]		  		





def validateEmail(email):
	if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email):
		raise argparse.ArgumentTypeError("Invalid email address.")
	return email


parser = argparse.ArgumentParser(description = 'Yet another email-resciever (via POP3 protocol).')
parser.add_argument('server_name', nargs = '?', help = 'POP3 server host name')
parser.add_argument('port', type = int, nargs = '?', help = 'POP3 server port')
parser.add_argument('username', type = validateEmail, nargs = '?', help = 'your email address')
parser.add_argument('password', nargs = '?', help = 'your password')
args = parser.parse_args()

pop3 = POP3(args.server_name, args.port)
pop3.authenticate(args.username, args.password)	
gui = GUI(title = 'Mail')
gui.mainloop()
pop3.closeConnection()

#docs: http://effbot.org/tkinterbook/tkinter-dialog-windows.htm	