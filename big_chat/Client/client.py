from authorization import AuthorizationWidget
from view import View
from model import Model

class Client(object):

    def __init__(self):
        self.__authWidget = AuthorizationWidget(self.authValidator)
        self.__view = View()
        self.__authWidget.show()

    def authValidator(self, login, password):
        if login == "":
            return "login is blank"

        if password == "":
            return "password is blank"

        if login.replace(' ','') == "":
            return "login contains only space"


       # server = "gmail.com"
        server = "localhost"
        #server = "vkmessenger.com"

        self.__model = Model()
        self.__view.setModel(self.__model)
        self.__model.setView(self.__view)
        if self.__model.auth(login, password, server):
            self.__model.connect(login, password, server)
        else:
            return "login or password is bad"

        self.__authWidget.close()
        self.__view.show()
        return True

client = Client()