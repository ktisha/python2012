import xmpp
import threading

class Model:
    def __init__(self):
        self.presence = dict()
        self.mess = ""

    def connect(self, user, password, server):
        self.user = user
        self.server = server
        self.connection.RegisterHandler('presence', self.presence_handler)
        self.connection.RegisterHandler('message', self.message_handler)
        self.connection.sendInitPresence()
        self.t1 = threading.Thread(target=self.handlerThread, args=(self.connection,))
        self.t1.start()
        print self.presence

    def auth(self, login, password, server):
        self.connection = xmpp.Client(server, debug=['socket'])
        self.connection.connect()
        jid = xmpp.JID(login)
        result = self.connection.auth(jid.getNode(), password, "LFY-client")
        if result == "sasl":
            return True
        return False

    def addPresence(self, login):
        self.presence[login] = 1
        self.view.userCome(login)
        print "add ", login

    def deletePresence(self, login):
        self.presence.pop(login)
        self.view.userLeave(login)

    def presence_handler(self, connect_object, message_node):
        to = message_node.attrs.get('to')
        frm = message_node.attrs.get('from')
        if(message_node.getType() == 'unavailable'):
            entry = str(frm.getStripped()) in self.presence
            if entry == False:
                return
            if str(frm.getStripped()) in self.presence:
                self.presence[str(frm.getStripped())] -= 1
            if self.presence[str(frm.getStripped())] == 0:
                self.deletePresence(str(frm.getStripped()))
        else:
            entry = str(frm.getStripped()) in self.presence
            if(str(frm.getStripped()) == self.user):
                return
            if entry is False:
                self.addPresence(str(frm.getStripped()))
            else:
                self.presence[str(str(frm.getStripped()))] += 1

    def message_handler(self, connect_object, message_node):
        if message_node.getTag('active') is not None and message_node.getBody() is not None:
            self.view.receiveMessage(message_node.getFrom().getStripped(), message_node.getBody())

    def handlerThread(self, connection):
        while connection.Process(1):
            pass

    def sendMessage(self, user, mess):
        mymsg = xmpp.protocol.Message(user, mess, "chat")
        self.connection.send(mymsg)

    def send(self, user, mess):
        self.mess = mess
        self.sendMessage(user, self.mess)

    def sendAll(self, mess):
        for user in self.presence:
            self.send(user, mess)

    def setView(self, _view):
        self.view = _view

