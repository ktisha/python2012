no_id = 0

class Man:
	def __init__(self):
		self.uid = no_id
		self.first_name = ""
		self.last_name = ""
	def __init__(self, id, f_name, l_name):
		self.uid = id
		self.first_name = f_name
		self.last_name = l_name

class CentralMan (Man):
	def __init__(self):
		pass
		
class Edge:
	def __init__(self):
		uid_start = no_id
		uid_end = no_id
	def __init__(self, uid_1, uid_2):
		uid_start = uid_1
		uid_end = uid_2

class EdgeRepost (Edge):
	def __init__(self):
		pass
		
class FriendsStar:
	def __init__(self, man, friends):
		self.central_man = man
		self.edges = {}
		self.other_men = {}
		for friend in friends:
			self.other_men[friend.uid] = friend
			self.edges[friend.uid] = set([])
	def addFriend(self, friend):
		self.other_men[friend.uid] = friend
		self.edges[friend.uid] = set([])

	

		
	
		