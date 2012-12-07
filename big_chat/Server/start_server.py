from twisted.internet import reactor
import logging
from server import ChatProtocolFactory

def start(host = 'localhost',port = 5222):
    logging.info( "Starting Server in " + host +":"+`port`)
    factory = ChatProtocolFactory(host)
    reactor.listenTCP(port, factory)
    reactor.run()

if __name__=="__main__":
    logging.basicConfig(level = logging.DEBUG)
    start()