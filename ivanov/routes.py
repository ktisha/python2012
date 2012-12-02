import bottle
import pymongo
import cgi
import re
import datetime
import random
import hmac
import json
import sys

import user
import achievement
import friend


connection_string = "mongodb://localhost"

@bottle.get('/')
def site_index():
	bottle.redirect("/main")

@bottle.get('/signup')
def present_signup():
	return bottle.template("signup", 
						   dict(username="", password="", 
								password_error="",
								username_value="",
								username_error=""))

@bottle.get('/login')
def present_login():
	return bottle.template("login", 
						   dict(username="", username_value="", password="", 
								login_error=""))

@bottle.get('/new_achievement')
def new_achievement():
	# check for a cookie, if present, then extract value
	username = login_check()
	if (username == None):
		print "main: can't identify user...redirecting to signup"
		bottle.redirect("/signup")
	return bottle.template("new_achievement", 
						   dict(name="", description="", tags="", username=username,
								name_error=""))

@bottle.get('/add_friend')
def add_friend():
	# check for a cookie, if present, then extract value
	username = login_check()
	if (username == None):
		print "main: can't identify user...redirecting to signup"
		bottle.redirect("/signup")
	return bottle.template("add_friend", 
						   dict(username=username, name_error=""))


@bottle.post('/login')
def process_login():
	connection = pymongo.Connection(connection_string, safe=True)

	username = bottle.request.forms.get("username")
	password = bottle.request.forms.get("password")

	userRecord = {}
	if (user.validate_login(connection, username, password, userRecord)):
		# looks good. start a new session
		session_id = user.start_session(connection, username)
		if (session_id == -1):
			bottle.redirect("/internal_error")

		cookie = user.make_secure_val(session_id)
		# send the cookie back to the user
		bottle.response.set_cookie("session", cookie)		
		# full round trip here.		
		bottle.redirect("/main")
	else:
		# not a valid login
		return bottle.template("login", 
						   dict(username_value=cgi.escape(username), password="", username="",
								login_error="Invalid Login"))


@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
	return ({error:"System has encountered a DB error"})

@bottle.get('/logout')
def process_logout():
	connection = pymongo.Connection(connection_string, safe=True)
	cookie = bottle.request.get_cookie("session")
	
	if (cookie == None):
		print "no cookie..."
		bottle.redirect("/login")
	else:
		session_id = user.check_secure_val(cookie)

		if (session_id == None):
			print "no secure session_id"
			bottle.redirect("/login")			
		else:
			# remove the session
			user.end_session(connection, session_id)
			print "clearing the cookie"
			bottle.response.set_cookie("session","")
			bottle.redirect("/login")

@bottle.post('/signup')
def process_signup():
	connection = pymongo.Connection(connection_string, safe=True)

	username = bottle.request.forms.get("username")
	password = bottle.request.forms.get("password")

	# set these up in case we have an error case
	errors = {'username_value':cgi.escape(username), 'username':''}
	if (user.validate_signup(username, password, errors)):
		if (not user.new_user(connection, username, password)):
			# this was a duplicate
			errors['username_error'] = "Username already in use. Please choose another"
			return bottle.template("signup", errors)
			
		session_id = user.start_session(connection, username)
		print session_id
		cookie = user.make_secure_val(session_id)
		bottle.response.set_cookie("session",cookie)
		bottle.redirect("/main")
	else:
		print "user did not validate"
		return bottle.template("signup", errors)

# will check if the user is logged in and if so, return the username. otherwise, it returns None
def login_check():
	connection = pymongo.Connection(connection_string, safe=True)
	cookie = bottle.request.get_cookie("session")

	if (cookie == None):
		print "no cookie..."
		return None

	else:
		session_id = user.check_secure_val(cookie)

		if (session_id == None):
			print "no secure session_id"
			return None			
		else:
			# look up username record
			session = user.get_session(connection, session_id)
			if (session == None):
				return None

	return session['username']
	
@bottle.get("/main")
def present_main():
	# check for a cookie, if present, then extract value
	username = login_check()
	if (username == None):
		print "main: can't identify user...redirecting to signup"
		bottle.redirect("/login")
	
	connection = pymongo.Connection(connection_string, safe=True)
	me = user.get_user(connection, username)
	friends = me['friends']
	friends_requests = me['friends_requests']
	challenges_ids = me['challenges']
	challenges = []
	for challenge_id in challenges_ids:
		challenges.append(achievement.find_achievement_by_id(connection, challenge_id))
	
	achievements_ids = me['achievements']
	achievements = []
	for achievement_id in achievements_ids:
		challenges.append(achievement.find_achievement_by_id(connection, achievement_id))
		
	return bottle.template("main", 
						{'username':username, 
						  'friends':friends,
						  'friends_requests':friends_requests,
						  'challenges':challenges,
						  'achievements':achievements,
						})

@bottle.post('/new_achievement')
def process_new_achievement():
	connection = pymongo.Connection(connection_string, safe=True)

	name = bottle.request.forms.get("name")
	description = bottle.request.forms.get("description")
	tags = bottle.request.forms.get("tags")

	my_username = login_check()
	try:
		username = bottle.request.query['to_user']
	except:
		username = my_username
	
	# set these up in case we have an error case
	errors = {'name':cgi.escape(name)}
	if (achievement.validate_new_achievement(name, errors)):
		id = achievement.new_achievement(connection, name, description, tags)
		if(username == my_username):
			print "to me"
			print id
			achievement.add_challenge_to_me(connection, my_username, id)
		else:
			print "to friend"
			achievement.add_challenge_to_friend(connection, username, my_username, id)
		bottle.redirect("/main")
	else:
		print "user did not validate"
		return bottle.template("new_achievement", errors)

@bottle.get("/search")
def search_resultts():	
	# check for a cookie, if present, then extract value
	username = login_check()
	if (username == None):
		print "main: can't identify user...redirecting to signup"
		bottle.redirect("/signup")
		
	try:
		query = bottle.request.query['q']
	except:
		query = ""
	connection = pymongo.Connection(connection_string, safe=True)
	achievements = achievement.find_achievements(connection, query)
	
	return bottle.template("search_results", q=query, username=username, achievements=achievements)

@bottle.get("/accept_friend_request")
def search_resultts():
	new_friend = bottle.request.query['friend']
	my_username = login_check()
	
	connection = pymongo.Connection(connection_string, safe=True)
	friend.accept_friend_request(connection, my_username, new_friend)
	
	bottle.redirect("/main")

@bottle.get("/reject_friend_request")
def search_resultts():
	new_friend = bottle.request.query['friend']
	my_username = login_check()
	
	connection = pymongo.Connection(connection_string, safe=True)
	friend.delete_friend_request(connection, my_username, new_friend)
	
	bottle.redirect("/main")

@bottle.post('/add_friend')
def add_friend():
	my_username = login_check()
	friend_username = bottle.request.forms.get("username")
	errors = {'username':cgi.escape(friend_username)}
	
	connection = pymongo.Connection(connection_string, safe=True)
	if (friend.new_friend_request(connection, my_username, friend_username, errors)):
		bottle.redirect("/main")
	else:
		return bottle.template("add_friend", errors)

@bottle.get("/delete_friend")
def search_resultts():
	new_friend = bottle.request.query['friend']
	my_username = login_check()
	
	connection = pymongo.Connection(connection_string, safe=True)
	friend.delete_friend(connection, my_username, new_friend)
	
	bottle.redirect("/main")

@bottle.get("/reject_challenge")
def search_resultts():
	challenge = bottle.request.query['challenge']
	my_username = login_check()
	
	connection = pymongo.Connection(connection_string, safe=True)
	achievement.reject_challenge(connection, my_username, challenge)
	
	bottle.redirect("/main")
	
@bottle.get("/accept_challenge")
def search_resultts():
	challenge = bottle.request.query['challenge']
	my_username = login_check()
	
	connection = pymongo.Connection(connection_string, safe=True)
	achievement.add_challenge_to_me(connection, my_username, challenge)
	
	bottle.redirect("/main")

# Static Routes
    #http://stackoverflow.com/questions/10486224/bottle-static-files
	#http://stackoverflow.com/questions/4237898/unicodedecodeerror-ascii-codec-cant-decode-byte-0xe0-in-position-0-ordinal
@bottle.get('/static/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static/css')

@bottle.get('/static/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return bottle.static_file(filename, root='static/img')

bottle.debug(True)
bottle.run(host='localhost', port=8082)


