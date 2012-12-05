__author__ = 'mazzachuses'

import xmpp

user = "XXXX@vk.com"
password = "q12345"
server = "localhost"

presence = set()

def message_handler(connect_object, message_node):
    #print "________",message_node.attrs
    pp = message_node
    to = pp.attrs.get('to')
    frm = pp.attrs.get('from')
    presence.add(frm)
    print "__________to: ", to, " from:", frm

#message = "idi sam nahui"
#connect_object.send( xmpp.Message( message_node.getFrom() ,message))

jid = xmpp.JID(user)
connection = xmpp.Client(server)
connection.connect()
result = connection.auth(jid.getNode(), password, "LFY-client")
connection.RegisterHandler('presence', message_handler)
connection.sendInitPresence()

mymsg = xmpp.protocol.Message("vladiev@localhost","hello","chat")
connection.send(mymsg)

while connection.Process(1):
    pass
