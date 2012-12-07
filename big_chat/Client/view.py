from PyQt4 import Qt
import datetime

class View(object):
    def __init__(self):
        if __name__ == "view":
            self.window = Qt.QWidget()
            self.window.setMinimumSize(450, 300)
            self.window.setWindowTitle("prototype client v0.03")

            self.rootHBoxLayout = Qt.QHBoxLayout()
            self.window.setLayout(self.rootHBoxLayout)

            self.chatVBoxLayout = Qt.QVBoxLayout()
            self.usersVBoxLayout = Qt.QVBoxLayout()

            self.rootHBoxLayout.addLayout(self.chatVBoxLayout)
            self.rootHBoxLayout.addLayout(self.usersVBoxLayout)

            self.usersLabel = Qt.QLabel("Users: ")
            self.usersLabel.setMaximumWidth(150)

            self.userList = Qt.QListWidget()
            self.userList.setFixedWidth(150)

            self.checkSendAll = Qt.QCheckBox()
            self.checkSendAll.setText("Send all")
            self.checkSendAll.setFixedWidth(150)

            self.usersVBoxLayout.addWidget(self.usersLabel)
            self.usersVBoxLayout.addWidget(self.userList)
            self.usersVBoxLayout.addWidget(self.checkSendAll)

            self.textEdit = Qt.QTextEdit()
            self.textEdit.setReadOnly(True)
            self.chatVBoxLayout.addWidget(self.textEdit)

            self.entryHBoxLayout = Qt.QHBoxLayout()
            self.chatVBoxLayout.addLayout(self.entryHBoxLayout)

            self.messageEdit = Qt.QLineEdit()
            self.sendBt = Qt.QPushButton("Send")
            self.sendBt.setFixedWidth(50)
            self.entryHBoxLayout.addWidget(self.messageEdit)
            self.entryHBoxLayout.addWidget(self.sendBt)

            Qt.QObject.connect(self.sendBt, Qt.SIGNAL("clicked()"), self.sendListener)
            Qt.QObject.connect(self.messageEdit, Qt.SIGNAL("returnPressed()"), self.sendListener)

    def userCome(self, login):
        index = 0
        while index < self.userList.count():
            if self.userList.item(index).text() == login:
                return
            index += 1
        self.userList.addItem(str(login))

    def userLeave(self, login):
        index = 0
        while index < self.userList.count():
            if self.userList.item(index).text() == login:
                self.userList.takeItem(index)
            index += 1

    def sendListener(self):
        if self.messageEdit.text() == "":
            self.textEdit.append("<B><FONT color='#ff0000'> you can't send empty message </FONT></B><BR>")
        else:
            dt = datetime.datetime.now()
            time = dt.strftime("%H:%M:%S")
            if self.checkSendAll.isChecked():
                self.textEdit.append("<B><FONT color='#654321'>I'm to all [" + time + '] </FONT></B><BR>' + self.messageEdit.text())
                self.model.sendAll(self.messageEdit.text())
            else:
                if self.userList.currentItem() == None:
                    self.userList.setCurrentItem(self.userList.item(0))
                self.model.send(str(self.userList.currentItem().text()), self.messageEdit.text())
                self.textEdit.append("<B><FONT color='#3caa3c'>To " + self.userList.currentItem().text() + " [" + time + '] </FONT></B><BR>' + self.messageEdit.text())
            self.messageEdit.clear()

    def show(self):
        self.window.show()

    def setModel(self, _model):
        self.model = _model

    def receiveMessage(self, login, message):
        dt = datetime.datetime.now()
        time = dt.strftime("%H:%M:%S")
        self.textEdit.append('<B><FONT color="#324862">' + login + ' [' + time + '] </FONT></B><BR>' + message)