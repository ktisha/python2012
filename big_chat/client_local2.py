#
#import xmpp
#
#user="cska63@vk.com"
#password="1993vovan"
#server="vkmessenger.com"
#
#def message_handler(connect_object, message_node):
#    message = "Welcome to my first Gtalk Bot :)"
#    connect_object.send( xmpp.Message( message_node.getFrom() ,message))
#
#jid = xmpp.JID(user)
#connection = xmpp.Client(server)
#connection.connect()
#result = connection.auth(jid.getNode(), password, "LFY-client")
#connection.RegisterHandler('message', message_handler)
#
#connection.sendInitPresence()
#
#while connection.Process(1):
#    pass


#
#import xmpp
#from xmpp.protocol import Message
#username = 'cska63'
#passwd = 'password'
#to='cska63@vk.com'
#msg='hello :)'
#
#
#
#client = xmpp.Client('gmail.com')
#client.connect(server=('talk.google.com',5223))
#client.auth(username, passwd, 'botty')
#client.sendInitPresence()
#message = xmpp.Message(to, msg)
#message.setAttr('type', 'chat')
#client.send(message)


#!/usr/bin/env python

#import xmpp
#
#user="cska631@gmail.com"
#password="vovan1993"
#server="gmail.com"
#
#jid = xmpp.JID(user)
#connection = xmpp.Client(server,debug=[])
#connection.connect()
#result = connection.auth(jid.getNode(), password,"LFY-client")
#print result
#connection.sendInitPresence()
#
#while connection.Process(1):
#    pass



import xmpp

user = "vladiev@vk.com"
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

while connection.Process(1):
    pass
