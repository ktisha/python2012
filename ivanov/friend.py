import cgi
import re
import hmac
import random
import string
import hashlib
import pymongo
import bson
import sys


def new_friend_request(connection, from_user, to_user, errors):
	db = connection.achievements_of_life
	users = db.users
	
	user = users.find({'_id':to_user})
	if(user==None):
		errors['username_error']  = "Username not found. Try another one"
		return False
	users.update({'_id':to_user}, { '$push' : { 'friends_requests' : from_user } })
	return True

def accept_friend_request(connection, user1_name, user2_name):
	db = connection.achievements_of_life
	users = db.users
	
	user1 = users.find_one({'_id':user1_name})
	user2 = users.find_one({'_id':user2_name})
	if((user1==None)or(user2==None)):
		return False
	
	delete_friend_request(connection, user1_name, user2_name)
	users.update({'_id':user1_name}, { '$push' : { 'friends' : user2_name } })
	users.update({'_id':user2_name}, { '$push' : { 'friends' : user1_name } })
	
	return True

def delete_friend_request(connection, user1_name, user2_name):
	db = connection.achievements_of_life
	users = db.users
	
	users.update({'_id':user1_name}, { '$pull' : { 'friends_requests' : user2_name } })
	users.update({'_id':user2_name}, { '$pull' : { 'friends_requests' : user1_name } })
	
	return True

def delete_friend(connection, user1_name, user2_name):
	db = connection.achievements_of_life
	users = db.users
	
	users.update({'_id':user1_name}, { '$pull' : { 'friends' : user2_name } })
	users.update({'_id':user2_name}, { '$pull' : { 'friends' : user1_name } })
	
	return True


def find_friends_of_user(connection, username):
	db = connection.achievements_of_life
	users = db.users
	
	me = None
	me = users.find_one({'_id':username, 'friends' : { '$exists' : True }}, fields=['friends'])
	if(me == None):
		return []
	
	return me['friends']

def find_friends_requests_of_user(connection, username):
	db = connection.achievements_of_life
	users = db.users
	
	me = None
	me = users.find_one({'_id':username, 'friends_requests' : { '$exists' : True }}, fields=['friends_requests'])
	if(me == None):
		return []
	
	return me['friends_requests']

def new_achievement(connection, name, description, category, tags):
	tags_splitted = tags.split(',')
	for tag in tags_splitted:
		tag.trim()
	
	achievement = {'name':name, 'description':description, 'category': category, 'tags':tags_splitted}
	
	db = connection.achievements_of_life
	achievements = db.achievements

	try:
		print "about to insert a new achievement %s", achievement
		achievements.insert(achievement)
	except pymongo.errors.OperationFailure:
		print "oops, mongo error"
		return False
	return True

SECRET = 'thisisnotsecret'
def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()

# call this to hash a cookie value
def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

# call this to make sure that the cookie is still secure
def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val
