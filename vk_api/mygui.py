# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import vk_api


class Example(QtGui.QMainWindow):

	def __init__(self):
		super(Example, self).__init__()

		self.initUI()

	def initUI(self):      

	
		QPushButton_read = QtGui.QPushButton("Read", self)
		QPushButton_read.move(100, 130)

		self.QLabel_UIDSFileName = QtGui.QLabel("UIDS file : ", self)
		self.QLabel_UIDSFileName.move(50, 40)
		self.QLineEdit_UIDSFileName = QtGui.QLineEdit(self)
		self.QLineEdit_UIDSFileName.setText("api.conf")
		self.QLineEdit_UIDSFileName.move(150, 40)
		
		self.QLabel_GDFFilePrefix = QtGui.QLabel("GDF file prefix : ", self)
		self.QLabel_GDFFilePrefix.move(50, 80)
		self.QLineEdit_GDFFilePrefix = QtGui.QLineEdit(self)
		self.QLineEdit_GDFFilePrefix.setText("")
		self.QLineEdit_GDFFilePrefix.move(150, 80)
		
		QPushButton_read.clicked.connect(self.read)            


		self.setGeometry(300, 300, 320, 190)
		self.setMinimumSize(320,190)
		self.setMaximumSize(320,190)
		self.setWindowTitle('Event sender')
		self.show()

	def read(self):
		pass
		uids_filename = self.QLineEdit_UIDSFileName.text()
		prefix = self.QLineEdit_GDFFilePrefix.text()
		self.vk_reader = vk_api.VKReader(uids_filename, prefix)
		self.vk_reader.read()
		
		

        
def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()