import re
import hmac
import random
import string
import hashlib
import pymongo
import pymongo.errors
import bson
import sys

# makes a little salt
def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt

# implement the function make_pw_hash(name, pw) that returns a hashed password
# of the format:
# HASH(pw + salt),salt
# use sha256
def make_pw_hash(pw, salt=None):
    if salt is None:
        salt = make_salt()
    return hashlib.sha256(pw + salt).hexdigest() + "," + salt

# validates that the user information is valid, return True of False
# and fills in the error codes
def validate_signup(username, password, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")

    errors['username_error'] = ""
    errors['password_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False

    return True

# validates the login, returns True if it's a valid user login. false otherwise
# to validate a login, the db must pull the user document and the hashed password
# and compare the password that the user has provided with the hashed password. to do the compare
# we must hash the password that the user is typing now on the login screen
def validate_login(connection, username, password, user_record):
    db = connection.achievements_of_life
    users = db.users

    user = None  # this is here to make sure code does not crash BEFORE assignment

    try:
        user = users.find_one({'_id': username})
    except TypeError, pymongo.errors.OperationFailure:
        print "Unable to query database for user"

    if user is None:
        print "User not in database"
        return False

    salt = user['password'].split(',')[1]

    if user['password'] != make_pw_hash(password, salt):
        print "user password is not a match"
        return False

    # looks good
    for key in user:
        user_record[key] = user[key] # perform a copy

    return True

# will start a new session id by adding a new document to the sessions collection
def start_session(connection, username):
    db = connection.achievements_of_life
    sessions = db.sessions

    session = {'username': username}

    try:
        sessions.insert(session)
    except pymongo.errors.OperationFailure:
        print "Unexpected error on start_session:", sys.exc_info()[0]
        return -1

    return str(session['_id'])

# will send a new user session by deleting from sessions table
def end_session(connection, session_id):
    db = connection.achievements_of_life
    sessions = db.sessions

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
        sessions.remove({'_id': id})
    except TypeError, bson.errors.InvalidId:
        return

# if there is a valid session, it is returned
def get_session(connection, session_id):
    db = connection.achievements_of_life
    sessions = db.sessions

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
    except TypeError, bson.errors.InvalidId:
        print "bad sessionid passed in"
        return None

    session = sessions.find_one({'_id': id})

    print "returning a session or none"
    return session


def get_user(connection, username):
    db = connection.achievements_of_life
    user = db.users.find_one({'_id': username})
    return user

# creates a new user in the database
def new_user(connection, username, password):
    # the hashed password is what we insert
    password_hash = make_pw_hash(password)

    user = {'_id': username, 'password': password_hash,
            'friends': [], 'friends_requests': [],
            'challenges': [],
            'challenges_requests_from_friends': [],
            'achievements': [],
            'achievements_requests_from_friends': [],
    }

    db = connection.achievements_of_life
    users = db.users

    try:
        print "inserting a user %s", user
        users.insert(user)
    except pymongo.errors.DuplicateKeyError:
        print "oops, username is already taken"
        return False
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
