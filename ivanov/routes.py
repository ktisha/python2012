from bottle import run, static_file, view, template, post, request, get, redirect, response, debug
import bson
import pymongo
import cgi

import user
import achievement
import friend

connection_string = "mongodb://localhost"

@get('/')
def site_index():
    redirect("/main")


@get('/signup')
def present_signup():
    return template("signup",
        dict(username="", password="",
            password_error="",
            username_value="",
            username_error=""))


@get('/login')
def present_login():
    return template("login",
        dict(username="", username_value="", password="",
            login_error=""))


@get("/achievement_unlocked_badge")
def achievement_unlocked_badge():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/signup")
    connection = pymongo.Connection(connection_string, safe=True)

    try:
        achievement_id = bson.objectid.ObjectId(request.query['achievement'])
        achievement_value = achievement.find_achievement_by_id(connection, achievement_id)
        return template("achievement_unlocked_badge",
            dict(username=username, achievement=achievement_value))
    except TypeError, bson.errors.InvalidId:
        redirect("/main")




@get('/new_achievement')
def new_achievement():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/signup")
    try:
        friend = request.query['friend']
    except KeyError:
        friend = ""
    return template("new_achievement",
        dict(name="", description="", tags="", username=username,
            name_error="", friend=friend))


@get('/add_friend')
def add_friend():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/signup")
    return template("add_friend",
        dict(username=username, username_error=""))


@post('/login')
def process_login():
    connection = pymongo.Connection(connection_string, safe=True)

    username = request.forms.get("username")
    password = request.forms.get("password")

    userRecord = {}
    if user.validate_login(connection, username, password, userRecord):
        # looks good. start a new session
        session_id = user.start_session(connection, username)
        if session_id is -1:
            redirect("/internal_error")

        cookie = user.make_secure_val(session_id)
        # send the cookie back to the user
        response.set_cookie("session", cookie)
        # full round trip here.
        redirect("/main")
    else:
        # not a valid login
        return template("login",
            dict(username_value=cgi.escape(username), password="", username="",
                login_error="Invalid Login"))


@get('/internal_error')
@view('error_template')
def internal_error():
    return {"error": "System has encountered a DB error"}


@get('/logout')
def logout():
    connection = pymongo.Connection(connection_string, safe=True)
    cookie = request.get_cookie("session")

    if cookie is None:
        print "no cookie..."
        redirect("/login")
    else:
        session_id = user.check_secure_val(cookie)

        if session_id is None:
            print "no secure session_id"
            redirect("/login")
        else:
            # remove the session
            user.end_session(connection, session_id)
            print "clearing the cookie"
            response.set_cookie("session", "")
            redirect("/login")


@post('/signup')
def signup():
    connection = pymongo.Connection(connection_string, safe=True)

    username = request.forms.get("username")
    password = request.forms.get("password")

    # set these up in case we have an error case
    errors = {'username_value': cgi.escape(username), 'username': ''}
    if user.validate_signup(username, password, errors):
        if not user.new_user(connection, username, password):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return template("signup", errors)

        session_id = user.start_session(connection, username)
        print session_id
        cookie = user.make_secure_val(session_id)
        response.set_cookie("session", cookie)
        redirect("/main")
    else:
        print "user did not validate"
        return template("signup", errors)

# will check if the user is logged in and if so, return the username. otherwise, it returns None
def login_check():
    connection = pymongo.Connection(connection_string, safe=True)
    cookie = request.get_cookie("session")

    if cookie is None:
        print "no cookie..."
        return None

    else:
        session_id = user.check_secure_val(cookie)

        if session_id is None:
            print "no secure session_id"
            return None
        else:
            # look up username record
            session = user.get_session(connection, session_id)
            if session is None:
                return None

    return session['username']


@get("/main")
def main():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/login")

    connection = pymongo.Connection(connection_string, safe=True)
    me = user.get_user(connection, username)
    friends = me['friends']
    friends_requests = me['friends_requests']
    challenges_ids = me['challenges']
    challenges = []
    for challenge_id in challenges_ids:
        challenges.append(achievement.find_achievement_by_id(connection, challenge_id))

    challenges_requests_ids = me['challenges_requests_from_friends']
    challenges_requests = []
    for challenge_id in challenges_requests_ids:
        challenge = {"achievement": achievement.find_achievement_by_id(connection, challenge_id['achievement']),
                     "from": challenge_id['from']}
        challenges_requests.append(challenge)

    achievements_ids = me['achievements']
    achievements = []
    for achievement_id in achievements_ids:
        achievements.append(achievement.find_achievement_by_id(connection, achievement_id))

    achievements_requests_ids = me['achievements_requests_from_friends']
    achievements_requests = []
    for achievement_id in achievements_requests_ids:
        achievement_id = {"achievement": achievement.find_achievement_by_id(connection, achievement_id['achievement']),
                          "from": achievement_id['from']}
        achievements_requests.append(achievement_id)

    return template("main",
        {'username': username,
         'friends': friends,
         'friends_requests': friends_requests,
         'challenges': challenges,
         'challenges_requests_from_friends': challenges_requests,
         'achievements': achievements,
         'achievements_requests_from_friends': achievements_requests
        })


@get("/friends")
def main():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/login")

    connection = pymongo.Connection(connection_string, safe=True)
    friend_name = None
    try:
        friend_name = request.query['friend']
    except KeyError:
        redirect("/main")

    friend = user.get_user(connection, friend_name)
    friends = friend['friends']
    challenges_ids = friend['challenges']
    challenges = []
    for challenge_id in challenges_ids:
        challenges.append(achievement.find_achievement_by_id(connection, challenge_id))

    achievements_ids = friend['achievements']
    achievements = []
    for achievement_id in achievements_ids:
        challenges.append(achievement.find_achievement_by_id(connection, achievement_id))

    me = user.get_user(connection, username)

    return template("friend",
        {'username': username,
         'friend': friend_name,
         'isFriend': friend_name in me['friends'],
         'friends': friends,
         'challenges': challenges,
         'achievements': achievements,
        })


@post('/new_achievement')
def new_achievement():
    connection = pymongo.Connection(connection_string, safe=True)

    name = request.forms.get("name")
    description = request.forms.get("description")
    tags = request.forms.get("tags")
    username = request.forms.get("friend")
    my_username = login_check()

    # set these up in case we have an error case
    errors = {'name': cgi.escape(name)}
    if achievement.validate_new_achievement(name, errors):
        id = achievement.new_achievement(connection, name, description, tags)
        if len(username) is 0:
            achievement.add_challenge_to_me(connection, my_username, id)
        else:
            achievement.add_challenge_to_friend(connection, username, my_username, id)
        redirect("/main")
    else:
        print "user did not validate"
        return template("new_achievement", errors)


@get("/search")
def search():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/signup")

    try:
        query = request.query['q']
    except KeyError:
        query = ""

    try:
        friend = request.query['friend']
    except KeyError:
        friend = ""

    connection = pymongo.Connection(connection_string, safe=True)
    achievements = achievement.find_achievements(connection, query)

    return template("search_results", friend=friend, q=query, username=username, achievements=achievements)


@get("/accept_friend_request")
def accept_friend_request():
    new_friend = request.query['friend']
    my_username = login_check()

    connection = pymongo.Connection(connection_string, safe=True)
    friend.accept_friend_request(connection, my_username, new_friend)

    redirect("/main")


@get("/reject_friend_request")
def reject_friend_request():
    new_friend = request.query['friend']
    my_username = login_check()

    connection = pymongo.Connection(connection_string, safe=True)
    friend.delete_friend_request(connection, my_username, new_friend)

    redirect("/main")


@post('/add_friend')
def add_friend():
    friend_username = request.forms.get("username")
    redirect("/add_friend_request?friend=" + friend_username)


@get('/add_friend_request')
def add_friend():
    my_username = login_check()

    friend_username = None
    try:
        friend_username = request.query['friend']
    except KeyError:
        redirect("/main")
    errors = {'username': cgi.escape(friend_username)}

    connection = pymongo.Connection(connection_string, safe=True)
    if friend.new_friend_request(connection, my_username, friend_username, errors):
        redirect("/main")
    else:
        return template("add_friend", errors)


@get("/delete_friend")
def delete_friend():
    new_friend = None
    try:
        new_friend = request.query['friend']
    except KeyError:
        redirect("/main")
    my_username = login_check()

    connection = pymongo.Connection(connection_string, safe=True)
    friend.delete_friend(connection, my_username, new_friend)

    redirect("/main")


@get("/reject_challenge")
def reject_challenge():
    challenge = request.query['challenge']
    my_username = login_check()

    connection = pymongo.Connection(connection_string, safe=True)
    achievement.reject_challenge(connection, my_username, challenge)

    redirect("/main")


@get("/accept_challenge")
def accept_challenge():
    challenge = request.query['challenge']
    my_username = login_check()
    connection = pymongo.Connection(connection_string, safe=True)

    try:
        friend_username = request.query['friend']
    except KeyError:
        friend_username = None

    if len(friend_username) is 0:
        achievement.add_challenge_to_me(connection, my_username, challenge)
    else:
        achievement.add_challenge_to_friend(connection, friend_username, my_username, challenge)
    redirect("/main")


@get("/add_challenge_from_friend")
def accept_challenge():
    challenge = request.query['challenge']
    my_username = login_check()
    connection = pymongo.Connection(connection_string, safe=True)
    achievement.add_challenge_from_friend(connection, my_username, challenge)
    redirect("/main")


@get("/reject_challenge_request")
def add_challenge_request():
    challenge = request.query['challenge']
    my_username = login_check()

    connection = pymongo.Connection(connection_string, safe=True)
    achievement.reject_challenge_from_friend(connection, my_username, challenge)
    redirect("/main")


@get("/achievement_unlocked")
def achievement_unlocked():
    achievement_id = request.query['achievement']
    my_username = login_check()
    connection = pymongo.Connection(connection_string, safe=True)

    try:
        friend_username = request.query['friend']
        achievement.unlock_achievement_to_friend(connection, friend_username, my_username, achievement_id)
        redirect("/friends?friend=" + friend_username)
    except KeyError:
        if achievement.unlock_achievement(connection, my_username, achievement_id):
            redirect("/achievement_unlocked_badge?achievement=" + achievement_id)
        else:
            redirect("/main")


@get("/unlock_achievement_from_friend")
def unlock_achievement_from_friend():
    achievement_id = request.query['achievement']
    my_username = login_check()
    connection = pymongo.Connection(connection_string, safe=True)
    if achievement.accept_achievement_unlock_from_friend(connection, my_username, achievement_id):
        redirect("/achievement_unlocked_badge?achievement=" + achievement_id)
    else:
        redirect("/main")


@get("/reject_achievement_request")
def reject_achievement_request():
    achievement_id = request.query['achievement']
    my_username = login_check()
    connection = pymongo.Connection(connection_string, safe=True)
    achievement.reject_achievement_unlock_from_friend(connection, my_username, achievement_id)
    redirect("/main")


# Static Routes
#http://stackoverflow.com/questions/10486224/static-files
#http://stackoverflow.com/questions/4237898/unicodedecodeerror-ascii-codec-cant-decode-byte-0xe0-in-position-0-ordinal
@get('/static/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')


@get('/static/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

debug(True)
run(host='localhost', port=8082)


