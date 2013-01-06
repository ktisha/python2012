#coding = utf-8
import httplib
import json
import time
access_token = "b502c74ae5c576c2b55ee74336b5300d71bb501b507c5cce5c2c7421c967390bb134dbc"

input_file = open("api.in", "r")
for word in input_file.readline().split():
	main_user_id = word
input_file.close()

output_file = open("api.out", "w")

request = "/method/friends.get?uid=" + main_user_id + "&access_token=" + access_token
print "sending request : ", request

#request = "/method/users.get?uids=211480,1305750&access_token=" + access_token
conn = httplib.HTTPSConnection("api.vkontakte.ru")
conn.request("GET", request)
reply = conn.getresponse()

print reply.status, reply.reason
#print reply.getheaders()

#str = reply.read()
#output_file.write(str)
main_friend_uids = []
for uid in json.loads(reply.read())['response']:
	#print uid
	main_friend_uids.append(uid)

	


packSize = 100
friends_in_pack = 0
pack = []
for main_friend_uid in main_friend_uids:
	if friends_in_pack >= packSize:
		request = "/method/users.get?uids="
		for uid in pack:
			request += str(uid)
			request += ","
		request += "&access_token=" + access_token
		print request
		conn.request("GET", request)
		reply = conn.getresponse()
		reply_string = reply.read()
		print reply_string
		
		friends = json.loads(reply_string)['response']
		for friend in friends:
			output_file.write(str(friend['uid']) + " " + str(friend['first_name'].encode('utf-8', 'ignore')) + " " + str(friend['last_name'].encode('utf-8', 'ignore')) + "\n")
		
		
		
		pack = []
		friends_in_pack = 0
		
	pack.append(main_friend_uid)
	friends_in_pack += 1
	

conn.close()
output_file.close()