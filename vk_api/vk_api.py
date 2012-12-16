# -*- coding: utf-8
import httplib
import json
import time
import vk_items
import MySQLdb
import argparse


class VKReader:
	def __init__(self, uids_filename, prefix):
		pass
		self.conf_file_name = uids_filename
		self.output_prefix = prefix


	def getToken(self):
		try:
			access_token_file = open("access_token.conf", "r")
			access_token = access_token_file.readline();
			access_token_file.close()
			return True, access_token
		except IOError:
			return False, "error getting token from file"
			
	def getCentralUID(self):
		try:
			uid_file = open(self.conf_file_name, "r")
			for word in uid_file.readline().split():
				uid = word
			uid_file.close()
			print "uid : ", uid
			return True, uid
		except IOError:
			return False, "error getting uid"

	def getManFriendsUIDs(self, uid, token):	
		request = "/method/friends.get?uid=" + str(uid) + "&access_token=" + token

		#print "sending request : ", request
		
		try:
			conn = httplib.HTTPSConnection("api.vkontakte.ru")
			conn.request("GET", request)
			reply = conn.getresponse()
		except:
			return False, "connection error"
			
		#print reply.status, reply.reason
		reply_string = reply.read()
		#print reply_string
		
		try:
			main_friend_uids = []
			for uid in json.loads(reply_string)['response']:
				main_friend_uids.append(uid)
		except:
			return False, "parsing error"
			
		conn.close()
		return True, main_friend_uids

	def getManFriends(self, uids, token):
		packSize = 100
		
		friends_in_pack = 0
		pack = []
		conn = httplib.HTTPSConnection("api.vkontakte.ru")
		result = []
		for main_uid in uids:
			if friends_in_pack >= packSize:
				
				request = "/method/users.get?uids="
				for uid in pack:
					request += str(uid)
					request += ","
				request += "&access_token=" + token

				conn.request("GET", request)
				reply = conn.getresponse()
				reply_string = reply.read()
				
				friends = json.loads(reply_string)['response']
				for friend in friends:
					result.append(vk_items.Man(friend['uid'], str(friend['first_name'].encode('utf-8', 'ignore')), str(friend['last_name'].encode('utf-8', 'ignore'))))
				pack = []
				friends_in_pack = 0
				
			pack.append(main_uid)
			friends_in_pack += 1
		if (len(uids) / packSize) * packSize != len(uids):
			request = "/method/users.get?uids="
			for uid in pack:
				request += str(uid)
				request += ","
			request += "&access_token=" + token

			conn.request("GET", request)
			reply = conn.getresponse()
			reply_string = reply.read()
			
			friends = json.loads(reply_string)['response']
			for friend in friends:
				result.append(vk_items.Man(friend['uid'], str(friend['first_name'].encode('utf-8', 'ignore')), str(friend['last_name'].encode('utf-8', 'ignore'))))
		
		conn.close()
		return True, result 

	def getMan(self, uid, token):
		request = "/method/users.get?uids=" + uid + "&access_token=" + token

		
		try:
			conn = httplib.HTTPSConnection("api.vkontakte.ru")
			conn.request("GET", request)
			reply = conn.getresponse()
		except:
			return False, "connection error"
			
		reply_string = reply.read()
		
		try:
			this_man = json.loads(reply_string)['response'][0]
			man = vk_items.Man(uid, str(this_man['first_name'].encode('utf-8', 'ignore')), str(this_man['last_name'].encode('utf-8', 'ignore')))
		except:
			return False, "parsing error"
			
		conn.close()
		return True, man
		
	def dropFriendsToFile(self, friends, filename):
		output_file = open(filename, "w")
		for friend in friends:
			output_file.write(str(friend.uid) + " " + friend.first_name + " " + friend.last_name + "\n")
		output_file.close()

	def printMan(self, man, output_file):
		output_file.write(str(man.uid) + " " + man.first_name + " " + man.last_name + "\n")


	def dropFriendsStarToFile(self, friends_star, filename):
		output_file = open(filename, "w")
		#print type(friends_star)
		self.printMan(friends_star.central_man, output_file)
		for man_uid in friends_star.other_men:
			self.printMan(friends_star.other_men[man_uid], output_file)
			for edge in friends_star.edges[man_uid]:
				output_file.write(str(edge) + "\n")
		output_file.close()

	def printManGDF(self, man, output_file):
		output_file.write(str(man.uid) + "," + man.first_name + "," + man.last_name + "\n")

	def printEdgeGDF(self, man_uid, other_man_uid, output_file):
		output_file.write(str(man_uid) + "," + str(other_man_uid)+ "\n")
		
		
	def dropFriendsStarToGDF(self, friends_star, filename):
		output_file = open(filename + ".gdf", "w")
		output_file.write("nodedef>name,first_name VARCHAR,last_name VARCHAR\n")
		self.printManGDF(friends_star.central_man, output_file)
		for man_uid in friends_star.other_men:
			self.printManGDF(friends_star.other_men[man_uid], output_file)
		output_file.write("edgedef> node1,node2\n")
		for man_uid in friends_star.other_men:
			for edge in friends_star.edges[man_uid]:
				self.printEdgeGDF(man_uid, edge, output_file)
		output_file.close()
		print "data exported to " + filename + ".gdf file"
		
	def printThings(self, things):
		for thing in things:
			print thing, "\n"

	def fillEdges(self, friends_star, max_num = 0):
		last_timing = time.time()
		for man_uid in friends_star.other_men:
			max_num -= 1;
			
			timing = time.time() - last_timing
			if timing < 0.34:
				time.sleep(0.34 - timing) #vk.com doesnt allow too frequent requests
			last_timing = time.time()
			
			print "asking for friends of ", friends_star.other_men[man_uid].last_name.decode('utf-8'), " ", friends_star.other_men[man_uid].first_name.decode('utf-8'), " uid : ", man_uid
			OK, his_friends = self.getManFriendsUIDs(man_uid, self.access_token)
			for somebody_uid in his_friends:
				if friends_star.other_men.has_key(somebody_uid):#i.e. this edge connects two men in the star
					friends_star.edges[man_uid].add(somebody_uid)
					friends_star.edges[somebody_uid].add(man_uid)
			if max_num == 0:
				break
		return friends_star

	def dropFriendsStarToMySQL(self, friends_star, hostname, username, password, databasename):
		db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=databasename, charset='utf8')
		cursor = db.cursor()
		

		sql = """INSERT INTO stars(time) VALUES ('%(time)s')"""%{"time":time.strftime('%x %X')}
		cursor.execute(sql)
		db.commit()
		
		sql = """select last_insert_id()"""
		cursor.execute(sql)
		db.commit()
		data =  cursor.fetchall()
		last_id = data[0][0]
		
		
		current_man = friends_star.central_man
		sql = """INSERT INTO men(uid, star_id, first_name, last_name) VALUES ('%(uid)s', '%(star_id)s', '%(first_name)s', '%(last_name)s')"""%{"uid":str(current_man.uid), "star_id":last_id, "first_name":current_man.first_name, "last_name":current_man.last_name}
		cursor.execute(sql)
		db.commit()
		
		for man_uid in friends_star.other_men:
			current_man = friends_star.other_men[man_uid]
			sql = """INSERT INTO men(uid, star_id, first_name, last_name) VALUES ('%(uid)s', '%(star_id)s', '%(first_name)s', '%(last_name)s')"""%{"uid":str(current_man.uid), "star_id":last_id, "first_name":current_man.first_name, "last_name":current_man.last_name}
			cursor.execute(sql)
			db.commit()
		for man_uid in friends_star.other_men:
			for edge in friends_star.edges[man_uid]:
				sql = """INSERT INTO edges(man_begin, star_id, man_end) VALUES ('%(star_id)s', '%(man_begin)s', '%(man_end)s')"""%{"star_id":last_id, "man_begin":man_uid, "man_end":edge}
				cursor.execute(sql)
				db.commit()
		db.close()
		print "data exported to MySQL database"

	def read(self):
		self.mysql_export = False


		parser = argparse.ArgumentParser()
		parser.add_argument("-mysqle", "--mysql_export", action='store_const', const=True, help="export data to mysql database")
		args = parser.parse_args()
		if args.mysql_export:
			self.mysql_export = True
			print("export to MySQL = true")
		else:
			print("export to MySQL = false")


		print time.strftime('%x %X')

		OK, self.access_token = self.getToken()
		if not OK:
			print "ERROR : ", self.access_token
			return

		#print "token : ", access_token, "\n"
			
		OK, main_user_id = self.getCentralUID()
		if not OK:
			print "ERROR : ", main_user_id
			return

		#print "main_user_id : ", main_user_id, "\n"

			
		OK, main_friend_uids = self.getManFriendsUIDs(main_user_id, self.access_token)
		if not OK:
			print "ERROR : ", main_friend_uids
			return

		#self.printThings(main_friend_uids)
			
			
		OK, friends = self.getManFriends(main_friend_uids, self.access_token)
		OK, centralMan = self.getMan(main_user_id, self.access_token)

		self.dropFriendsToFile(friends, "api.out")

		friends_star = vk_items.FriendsStar(centralMan, friends)
		friends_star = self.fillEdges(friends_star, 0)

		#print type(friends_star)
		#self.dropFriendsStarToFile(friends_star, "apiStar.out")
		self.dropFriendsStarToGDF(friends_star, self.output_prefix+"_out_" + str(main_user_id))
		if self.mysql_export:
			self.dropFriendsStarToMySQL(friends_star, '127.0.0.1', 'root', 'root', 'vk_items')


