from PyQt4 import Qt
from PyQt4 import QtCore


class AuthorizationWidget(object):
    def __init__(self, validationFunc):
        if __name__ == "authorization":
            self.validationFunc = validationFunc
            self.window = Qt.QWidget()
            self.window.setWindowTitle("authorization")

            self.layout = Qt.QVBoxLayout()
            self.layout.setContentsMargins(10, 15, 10, 15)
            self.layout.setSpacing(7)
            self.window.setLayout(self.layout)

            self.label1 = Qt.QLabel("Enter your nickname:")
            self.label1.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.label1)

            self.editNickname = Qt.QLineEdit()
            self.layout.addWidget(self.editNickname)

            self.label2 = Qt.QLabel("Enter your password:")
            self.label2.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.label2)

            self.editPassword = Qt.QLineEdit()
            self.editPassword.setEchoMode(2)
            self.layout.addWidget(self.editPassword)

            self.serverListLayout = Qt.QHBoxLayout()
            self.serverListLabel = Qt.QLabel("Server:")
            self.serverListLabel.setFixedWidth(35)
            self.serverList = Qt.QComboBox()
            servers = QtCore.QStringList(["gmail.com", "vkmessenger.com", "localhost"])
            self.serverList.addItems(servers)
            self.serverListLayout.addWidget(self.serverListLabel)
            self.serverListLayout.addWidget(self.serverList)

            self.layout.addLayout(self.serverListLayout)

            self.bt1 = Qt.QPushButton("Ok")
            self.layout.addWidget(self.bt1)

            self.labelError = Qt.QLabel('')
            self.labelError.setAlignment(QtCore.Qt.AlignCenter)
            self.labelError.hide()
            self.layout.addWidget(self.labelError)

            Qt.QObject.connect(self.bt1, Qt.SIGNAL("clicked()"), self.okBtListener)
            Qt.QObject.connect(self.editNickname, Qt.SIGNAL("returnPressed()"), self.okBtListener)
            Qt.QObject.connect(self.editPassword, Qt.SIGNAL("returnPressed()"), self.okBtListener)

    def okBtListener(self):
        result = self.validationFunc(str(self.editNickname.text()), str(self.editPassword.text()),
            str(self.serverList.itemText(self.serverList.currentIndex())))
        if result != True:
            self.labelError.setText('<B><FONT color="red">%s</FONT></B>' % result)
            self.labelError.show()

    def close(self):
        Qt.QObject.disconnect(self.bt1, Qt.SIGNAL("clicked()"), self.okBtListener)
        Qt.QObject.disconnect(self.editNickname, Qt.SIGNAL("returnPressed()"), self.okBtListener)
        Qt.QObject.disconnect(self.editPassword, Qt.SIGNAL("returnPressed()"), self.okBtListener)
        self.window.close()

    def show(self):
        self.window.show()

