from authorization import AuthorizationWidget
from view import View
from model import Model
from PyQt4 import Qt
import sys

class Client(object):
    def __init__(self):
        self.app = Qt.QApplication(sys.argv)
        self.__authWidget = AuthorizationWidget(self.authValidator)
        self.__view = View(self.app)
        self.__authWidget.show()
        self.app.exec_()

    def authValidator(self, login, password, server):
        if login == "":
            return "login is empty"

        if password == "":
            return "password is empty"

        if login.replace(' ', '') == "":
            return "login contains only spaces"

        if server == "vkmessenger.com":
            login += "@vk.com"
        else:
            if server == "gmail.com":
                login += "@gmail.com"
            else:
                if server == "localhost":
                    login += "@localhost.ru"

        self.__model = Model()
        self.__view.setModel(self.__model)
        self.__model.setView(self.__view)
        if self.__model.auth(login, password, server):
            self.__model.connect(login, password, server)
        else:
            return "login or password is invalid"

        self.__authWidget.close()
        self.__view.show()
        return True

client = Client()