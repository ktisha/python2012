from bottle import run, static_file, view, template, post, request, get, redirect, response, debug
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


@get('/new_achievement')
def new_achievement():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/signup")
    return template("new_achievement",
                    dict(name="", description="", tags="", username=username,
                         name_error=""))


@get('/add_friend')
def add_friend():
    # check for a cookie, if present, then extract value
    username = login_check()
    if username is None:
        print "main: can't identify user...redirecting to signup"
        redirect("/signup")
    return template("add_friend",
                    dict(username=username, name_error=""))


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

    achievements_ids = me['achievements']
    achievements = []
    for achievement_id in achievements_ids:
        challenges.append(achievement.find_achievement_by_id(connection, achievement_id))

    return template("main",
                    {'username': username,
                     'friends': friends,
                     'friends_requests': friends_requests,
                     'challenges': challenges,
                     'achievements': achievements,
                    })


@post('/new_achievement')
def new_achievement():
    connection = pymongo.Connection(connection_string, safe=True)

    name = request.forms.get("name")
    description = request.forms.get("description")
    tags = request.forms.get("tags")

    my_username = login_check()
    try:
        username = request.query['to_user']
    except KeyError:
        username = my_username

    # set these up in case we have an error case
    errors = {'name': cgi.escape(name)}
    if achievement.validate_new_achievement(name, errors):
        id = achievement.new_achievement(connection, name, description, tags)
        if username is my_username:
            print "to me"
            print id
            achievement.add_challenge_to_me(connection, my_username, id)
        else:
            print "to friend"
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
    connection = pymongo.Connection(connection_string, safe=True)
    achievements = achievement.find_achievements(connection, query)

    return template("search_results", q=query, username=username, achievements=achievements)


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
    my_username = login_check()
    friend_username = request.forms.get("username")
    errors = {'username': cgi.escape(friend_username)}

    connection = pymongo.Connection(connection_string, safe=True)
    if friend.new_friend_request(connection, my_username, friend_username, errors):
        redirect("/main")
    else:
        return template("add_friend", errors)


@get("/delete_friend")
def delete_friend():
    new_friend = request.query['friend']
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
    achievement.add_challenge_to_me(connection, my_username, challenge)

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


