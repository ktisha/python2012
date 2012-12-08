#coding: utf-8

import socket as sck
import base64
import ssl
import logging
logging.basicConfig(level = logging.INFO)


class SMTP:	

	def __init__(self, server_name, port):
		self.connect(server_name, port)			
		self.use_secure = False

	def connect(self, server_name, port):
		self.socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
		logging.debug('before connect')
		logging.debug(server_name + ' ' + str(port))
		self.socket.connect((server_name, port))		
		logging.info('reply: ' + self.socket.recv(256))
		logging.debug('connected')

	def getProperSocket(self):
		if self.use_secure:
			return self.secure_socket
		return self.socket		

	def sendCommand(self, cmd, body=''):
		socket = self.getProperSocket()

		cmds_to_escape = 'MAIL FROM', 'RCPT TO', 'SEND FROM', 'SOML FROM', 'SAML FROM'
		single_cmds = 'DATA', 'RSET', 'NOOP', 'QUIT', 'STARTTLS'

		for cmd_esc in cmds_to_escape:
			if cmd == cmd_esc:
				cmd = cmd + ':'
				body = '<' + body + '>'
				break		

		for cmd_single in single_cmds:
			if cmd == cmd_single:				
				break
		else:			
			body = ' ' + body

		socket.send(cmd + body + '\r\n')
		logging.debug(cmd + body + ' cmd sent')
		reply = socket.recv(256)
		logging.info('reply: ' + reply)
		return reply

	def sendText(self, sender, reciever, subj, msg):		
		socket = self.getProperSocket()
		header = 'From: ' + sender + ' <' + sender + '>' + '\nTo: ' + reciever + '\n'						
		subject = 'Subject: ' + subj + '\n'				
		socket.send(header + subject + '\r\n' + msg + '\r\n.\r\n')		
		logging.debug(header + subject + msg + ' ----- message sent')
		logging.info('reply: ' + socket.recv(100))

	def authLogin(self, username, password):
		socket = self.getProperSocket()

		auth_reply = self.sendCommand('AUTH LOGIN')
		if auth_reply[:3] != '334':
			raise Exception('AUTH LOGIN server response is unrecognizable.')
		if base64.b64decode(auth_reply[4:]) != 'Username:':
			raise Exception('AUTH LOGIN unsupported syntax.')

		socket.send(base64.b64encode(username) + '\r\n')
		username_reply = socket.recv(256)				
		if username_reply[:3] != '334':
			raise Exception('AUTH LOGIN server response is unrecognizable.')
		if base64.b64decode(username_reply[4:]) != 'Password:':
			raise Exception('AUTH LOGIN unsupported syntax.')
						
		socket.send(base64.b64encode(password) + '\r\n')
		password_reply = socket.recv(256)
		logging.debug(password_reply)
		if password_reply[:3] != '235':					
			raise Exception('Wrong username or password')

	def startTLSNegotiation(self, username, password):
		reply = self.sendCommand('STARTTLS')		
		if reply[:3] != '220':
			raise Exception('STARTTLS server response is unrecognizable')
		self.secure_socket = ssl.wrap_socket(self.socket, ssl_version = ssl.PROTOCOL_SSLv23)
		self.use_secure = True
		self.authLogin(username, password)


	def sendMessage(self, sender, reciever, subject, msg, password):		
		hostName = self.getHostName()
		ehlo_reply = self.sendCommand('EHLO', hostName)		

		auth_enabled = False
		auth_pos = ehlo_reply.find('AUTH')		
		starttls_pos = ehlo_reply.find('STARTTLS')	
		# смотрим, поддерживает ли сервер аутентификацию
		if starttls_pos != -1:
			self.startTLSNegotiation(sender, password)
			auth_enabled = True
		elif auth_pos != -1:			
			# рассчитываем на поддержку AUTH LOGIN
			if ehlo_reply.find('LOGIN') != -1:	
				self.authLogin(sender, password)
				auth_enabled = True
			else:
				raise Exception('AUTH type is unsupported.')								

		self.sendCommand('MAIL FROM', sender)
		self.sendCommand('RCPT TO', reciever)
		self.sendCommand('DATA')		
		self.sendText(sender, reciever, subject, msg)		
		self.sendCommand('QUIT')
		return auth_enabled

	def getHostName(self):		
		#получаем свой айпи
		s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)	
		s.connect(("gmail.com", 80))		
		hostName = s.getsockname()[0]		
		s.close()
		return hostName

	def close(self):
		self.socket.close()		
		logging.debug('connection closed')