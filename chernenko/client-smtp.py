#coding: utf-8

from smtp import *
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
		dim['width'] = 600
		dim['height'] = 400		
		self.minsize(dim['width'], dim['height'])
		self.maxsize(dim['width'], dim['height'])		

		dim['gap_x'] = dim['gap_y'] = 10
		dim['fields_height'] = 26
		dim['label_width'] = 70
		dim['btn_width'] = 60

		self.createWidgets()
	
	def createWidgets(self):
		dim = self.dimensions

		panel_frame = Frame(self, height = 2 * dim['gap_y'] + 3 * dim['fields_height'])		
		text_frame = Frame(self, height = dim['height'] - panel_frame['height'], width = dim['width'])

		panel_frame.pack(side = 'top', fill = 'x')
		text_frame.pack(side = 'bottom', fill = 'both', expand = 1)

		self.textbox = Text(text_frame, font = font, wrap = 'word')
		scrollbar = Scrollbar(text_frame)

		scrollbar['command'] = self.textbox.yview
		self.textbox['yscrollcommand'] = scrollbar.set

		self.textbox.pack(side = 'left', fill = 'both', expand = 1)
		scrollbar.pack(side = 'right', fill = 'y')		

		from_label = Label(panel_frame, text = 'From: ', font = font)
		to_label = Label(panel_frame, text= 'To: ', font = font)
		subject_label = Label(panel_frame, text = 'Subject: ', font = font)

		self.from_entry = Entry(panel_frame, font = font)
		self.from_entry.insert(0, args.username)
		self.from_entry.config(state = DISABLED)
		self.to_entry = Entry(panel_frame, font = font)		
		self.subject_entry = Entry(panel_frame, font = font)
		self.subject_entry.insert(0, '')

		from_label.place(x = dim['gap_x'], y = dim['gap_y'], height = dim['fields_height'])
		to_label.place(x = dim['gap_x'], y = dim['gap_y'] + dim['fields_height'], height = dim['fields_height'])
		subject_label.place(x = dim['gap_x'], y = dim['gap_y'] + 2 * dim['fields_height'], height = dim['fields_height'])

		entry_width = dim['width'] - dim['label_width'] - dim['btn_width'] - 3 * dim['gap_x']	
		self.from_entry.place(x = dim['gap_x'] + dim['label_width'], y = dim['gap_y'], height = dim['fields_height'], width = entry_width)
		self.to_entry.place(x = dim['gap_x'] + dim['label_width'], y = dim['gap_y'] + dim['fields_height'], height = dim['fields_height'], width = entry_width)
		self.subject_entry.place(x = dim['gap_x'] + dim['label_width'], y = dim['gap_y'] + 2 * dim['fields_height'], height = dim['fields_height'], width = entry_width)

		self.send_btn = Button(panel_frame, text = 'Send', font = font, command = self.send)		
		self.send_btn.place(x = dim['width'] - dim['btn_width'] - dim['gap_x'], y = panel_frame['height'] / 3, width = dim['btn_width'])			
		  	
	def send(self):		
		try:				
			if self.to_entry.get() != '':
				auth_support = smtp.sendMessage(self.from_entry.get(), self.to_entry.get(), self.subject_entry.get(), self.textbox.get('1.0', 'end'), args.password)	
				if auth_support is False:
					tkMessageBox.showinfo('Auth', 'Aunthentication is unsupported for this smtp server.')
				tkMessageBox.showinfo('Sending...', 'Message sent.')
			else:
				tkMessageBox.showwarning('Empty field', 'The reciever mail address is unspecified.')			
		except Exception as e:		
			tkMessageBox.showwarning('Error', str(e) + '\nFix the mistakes or try later.')				





def validateEmail(email):
	if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email):
		raise argparse.ArgumentTypeError("Invalid email address.")
	return email


parser = argparse.ArgumentParser(description = 'Yet another email-sender (via SMTP protocol).')
parser.add_argument('server_name', nargs = '?', help = 'SMTP server host name')
parser.add_argument('port', type = int, nargs = '?', help = 'SMTP server port')
parser.add_argument('username', type = validateEmail, nargs = '?', help = 'sender email address')
parser.add_argument('--password', nargs = '?', help = 'sender password if aunthentication is provided by server')
args = parser.parse_args()

smtp = SMTP(args.server_name, args.port)
gui = GUI(title = 'Mail')
gui.mainloop()
smtp.close()

#docs: http://effbot.org/tkinterbook/tkinter-dialog-windows.htm	