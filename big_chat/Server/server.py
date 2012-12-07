from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.web.sux import XMLParser
import base64
from stanza import Stanza
import logging
#todo decorator
def get_step(number):
    file = open("Steps/step" + str(number) + ".xml")
    res = file.read()
    file.close()
    return res


class XMLChatProtocol(XMLParser):
    def __init__(self):
        self.username = None
        self.realm = None
        self.login_res = None
        self.login = None

        self.id = None
        self.stack_stanzas = []
        self.success_auth = False
        self.resource = None

    def get_user_name(self):
        return self.username

    def gotTagStart(self, name, attributes):
    # XMLParser.gotTagStart(self, name, attributes)
        stanza = Stanza(name, attributes)
        self.stack_stanzas.append(stanza)
        self.__handle_()

    def __handle_(self):
        stack = self.stack_stanzas
        stanza = stack.pop()
        logging.debug("got stanza:" + stanza.to_xml())
        if stanza.is_closed():
            if stanza.get_name() == "auth":
                self.__send_(get_step(3))
            elif stanza.get_name() == "response":
                self.handle_response(stanza)
            elif stanza.get_name() == "iq":
                self.handle_query(stanza)
            elif stanza.get_name() == "message":
                self.__handle_message_(stanza)
            elif stanza.get_name() == "presence":
                self.__handle_presence_(stanza)
            stack[len(stack) - 1].add_child(stanza)


        else:
            if stanza.get_name() == "stream:stream":
                if not self.success_auth:
                    self.id = self.factory.get_id()
                    host = self.factory.get_host()
                    response = get_step(1) % (self.id, host)
                    self.__send_(response)
                    self.__send_(get_step(2))
                if self.success_auth: #end auth and add user
                    host = self.factory.get_host()
                    response = get_step(6) % (self.id, host)
                    self.__send_(response)

            stack.append(stanza)

    def __send_(self, data):
        logging.debug("send:" + data)
        self.transport.write(data)

    def __handle_presence_(self, stanza):
        map = self.factory.get_clients()
        for client in map.items():
            if client[0] != self.username:
                client[1].report_presence(self)


    def __handle_message_(self, stanza):
        attrs = stanza.get_attrs()
        to = attrs['to'].split("@")[0]
        user = self.factory.get_client(to)
        if user:
            attrs['to'] = user.login
            attrs['from'] = self.username + '@' + self.realm
            attrs['xml:lang'] = 'en'
            stanza.add_child(Stanza('active', {'xmlns': 'http://jabber.org/protocol/chatstates'}))
            user.__send_(stanza.to_xml())

    def handle_response(self, stanza):
        if not self.success_auth:
            data = base64.b64decode(stanza.get_text()).split(",")
            for entry in data:
                if entry.startswith("username"):
                    self.username = entry.split("=")[1].replace("'", "").replace('"', '')
                if entry.startswith("realm"):
                    self.realm = entry.split("=")[1].replace("'", "").replace('"', '')
            if not self.factory.has_user(self.username):
                self.__send_(get_step(4))
                self.success_auth = True
            else:
                self.__send_(get_step(100))
                self.transport.loseConnection()
        else:
            self.__send_(get_step(5))


    def handle_query(self, stanza):
        attrs = stanza.get_attrs()
        id = attrs["id"]
        type = attrs["type"]
        if type == "set":
            child1 = stanza.get_children()[0]
            if child1.get_name() == "bind":
                resource = child1.get_children()[0]
                del child1.get_children()[0]
                self.resource = resource.get_text()
                response = Stanza("iq", {'id': id, 'type': 'result'})
                self.login_res = self.username + "@" + self.realm + "/" + self.resource
                self.login = self.username + "@" + self.realm
                self.add_user()
                jid = Stanza("jid", text=self.login_res)
                child1.add_child(jid)
                response.add_child(child1)
                self.__send_(response.to_xml())
            elif child1.get_name() == "session":
                response = Stanza("iq", {'from': self.realm, 'type': 'result', "id": id})
                self.__send_(response.to_xml())
            else:
                stanza = Stanza("iq",
                    {'type': 'error', 'from': self.factory.get_host(), 'id': id, 'to': self.login_res})
        elif type == "get":
            for child in stanza.get_children():
                if child.get_name() == "query":
                    query = child
                    if query.get_attr("xmlns") == "jabber:iq:roster":
                        response = Stanza("iq", {"to": self.login_res, type: "result", "id": id})
                        response.add_child(query)
                        for user in self.factory.get_clients().items():
                            if user[0] != self.username:
                                item = Stanza("item",
                                    {'jid': user[1].login, 'name': user[1].username, 'subscription': 'both'})
                                query.add_child(item)

                        self.__send_(response.to_xml())
                        for user in self.factory.get_clients().items():
                            if user[0] != self.username:
                                presence = Stanza("presence", {'from': user[1].login, 'to': self.login_res})
                                self.__send_(presence.to_xml())
                    else:
                        stanza = Stanza("iq",
                            {'type': 'error', 'from': self.factory.get_host(), 'id': id, 'to': self.login_res})
                        stanza.add_child(query)
                        self.__send_(stanza.to_xml())

    def connectionLost(self, reason):
        self.report_presence_unavailable()
        self.factory.remove_user(self.username)
        #  XMLParser.connectionLost(self,reason)


    def report_presence(self, other_user):
        stanza = Stanza("presence", {'from': other_user.login, 'to': self.login_res})
        self.__send_(stanza.to_xml())

    def report_presence_unavailable(self):
        for user in self.factory.get_clients().items():
            stanza = Stanza("presence", {'from': self.login, 'to': user[1].login_res, 'type': 'unavailable'})
            user[1].__send_(stanza.to_xml())


    def add_user(self):
        self.factory.add_client(self)


    def gotTagEnd(self, name):
    # XMLParser.gotTagEnd(self, name)
        stack = self.stack_stanzas
        stanza = stack.pop()
        stanza.close()
        stack.append(stanza)
        self.__handle_()


    def gotText(self, data):
    # XMLParser.gotText(self, data)
        length = len(self.stack_stanzas)
        if length > 0:
            self.stack_stanzas[length - 1].add_text(data)


class ChatProtocolFactory(ServerFactory):
    protocol = XMLChatProtocol


    def __init__(self, host):
        self.__clients_ = {} #user_name - > XMLChatProtocol todo add support resourses
        self.__host_ = host
        self.__cur_id_ = -1

    def sendMessageToAllClients(self, mesg):
        for client in self.clientProtocols:
            client.sendLine(mesg)

    def get_host(self):
        return self.__host_

    def get_id(self):
        self.__cur_id_ += 1
        return self.__cur_id_

    def add_client(self, user):
        self.__clients_[user.get_user_name()] = user

    def get_clients(self):
        return self.__clients_

    def get_client(self, user_name):
        if self.__clients_.has_key(user_name):
            return self.__clients_[user_name]
        else:
            return None

    def has_user(self, name):
        return self.__clients_.has_key(name)

    def remove_user(self, username):
        del self.__clients_[username]


