#coding: utf-8

import socket as sck
import sys
import base64
import ssl
from email.header import decode_header
import logging
logging.basicConfig(level = logging.DEBUG)


class Message:
	def __init__(self, msg):
		self.msg = msg;

	def truncate(self):
		#убираем последнюю непустую строку - служебный разделитель
		spaces = set(' \t\r\n')		
		for msg_id, char in enumerate(reversed(self.msg)):
			if char not in spaces:
				p = self.msg[:len(self.msg) - msg_id].rfind('\n')
				return self.msg[:p]

	def parse(self):
		#отрезаем лишнее, оставляем только чистый текст
		key_phrase = 'Content-Type: text/plain'
		p_start = self.msg.find(key_phrase)		
		if p_start == -1:
			if self.msg.find('Content-Type: ') != -1:
				return 'This message format is unsupported'
			return self.msg
		
		p_start = self.msg.find('\n', p_start) + 1
		p_end = self.msg.find('Content-Type: ', p_start)
		self.msg = self.msg[p_start:p_end]
		return self.truncate()

class Utils:
	def decodeString(self, string):		
		dh = decode_header(string)
		return ''.join([ unicode(t[0], t[1] or 'ASCII') for t in dh ])

	def copyContent(self, key_word, original, stop_word = '\r\n'):
		start = original.find(key_word)
		end = original.find(stop_word, start)		
		return original[start + len(key_word):end]

	def parseHeader(self, header):
		result = dict()
		result.update({'date': utils.copyContent('Date:', header)})
		result.update({'from': utils.decodeString(utils.copyContent('From:', header))})
		result.update({'subject': utils.decodeString(utils.copyContent('Subject:', header))})		
		return result

utils = Utils()


class POP3:	

	def __init__(self, server_name, port):
		self.connect(server_name, port)			
		self.use_secure = False

	def connect(self, server_name, port):
		self.socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
		if port != 110:
			self.socket = ssl.wrap_socket(self.socket, ssl_version = ssl.PROTOCOL_SSLv23)
			self.use_secure = True
		logging.debug('before connect')
		logging.debug(server_name + ' ' + str(port))
		self.socket.connect((server_name, port))		
		logging.info('reply: ' + self.socket.recv(200))
		logging.debug('connected')

	def sendCommand(self, cmd, body = ''):		
		single_cmds = 'STAT', 'RSET', 'QUIT', 'NOOP'
		
		for cmd_single in single_cmds:
			if cmd == cmd_single:		
				break
		else:
			body = ' ' + body

		self.socket.send(cmd + body + '\r\n')
		logging.debug(cmd + body + ' cmd sent')							
		reply = self.socket.recv(200)		
		logging.debug('reply: ' + reply)
		return reply	

	def getBigReply(self):
		reply = []
		while True:
			buf = self.socket.recv(1024)
			reply.append(buf)
			if buf.endswith('\r\n.\r\n'):
				break
		reply = ''.join(reply)
		if reply[:3] != '+OK':				
			raise Exception('This pop3 server is unsupported') #TODO
		return reply

	def recieveHeader(self, msg_id):
		self.socket.send('TOP ' + str(msg_id) + ' 0' + '\r\n')
		logging.debug('TOP ' + str(msg_id) + ' 0' + ' cmd sent')
		reply = self.getBigReply()
		header = reply[:len(reply) - 3]		
		meta = utils.parseHeader(header)			
		return meta, header

	def recieveMessageText(self, msg_id):
		meta, header = self.recieveHeader(msg_id)		
		
		self.socket.send('RETR ' + str(msg_id) + '\r\n')
		logging.debug('RETR ' + str(msg_id) + ' cmd sent')
		reply = self.getBigReply()
		msg = reply[len(header):len(reply) - 3]
		msg = Message(msg)
		msg = msg.parse()
		return meta, msg

	def getMessageNumber(self):
		reply = self.sendCommand('STAT')
		if reply[:3] != '+OK':
			Exception('Something went wrong. Try later')
		tokens = reply.split()
		return int(tokens[1])

	def authenticate(self, username, password):
		if self.use_secure:
			self.secureAuth(username, password)
		else:
			self.simpleAuth(username, password)

	def simpleAuth(self, username, password):
		self.sendCommand('USER', username)
		self.sendCommand('PASS', password)	
		
	def receiveMessage(self, msg_id):		
		return self.recieveMessageText(msg_id)		

	def closeConnection(self):
		self.sendCommand('QUIT')

	



if __name__ == '__main__':
	pop3 = POP3(sys.argv[1], int(sys.argv[2]))
	pop3.authenticate(sys.argv[3], sys.argv[4])	
	meta, msg = pop3.receiveMessage(19)	
	print meta, msg
	pop3.closeConnection()