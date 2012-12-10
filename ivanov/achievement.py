import re
import pymongo
import pymongo.errors
import bson

def validate_new_achievement(name, errors):
    NAME_RE = re.compile("^.+$")

    errors['name_error'] = ""

    if not NAME_RE.match(name):
        errors['name_error'] = "empty name. fill this field, please"
        return False

    return True


def find_achievement_by_id(connection, achievement_id):
    db = connection.achievements_of_life
    achievements = db.achievements
    result = achievements.find_one({'_id': achievement_id})
    return result


def find_achievements(connection, query):
    db = connection.achievements_of_life
    achievements = db.achievements

    result = None
    if len(query) is 0:
        return result

    regex = re.compile(query, re.IGNORECASE)
    result = achievements.find({'$or': [{'tags': query}, {'name': regex}]})

    print "returning found achievements or none"
    return result


def new_achievement(connection, name, description, tags):
    tags_splinted = tags.split(',')
    map(lambda x: x.strip(), tags_splinted)

    achievement = {'name': name, 'description': description, 'tags': tags_splinted}

    db = connection.achievements_of_life
    achievements = db.achievements

    try:
        print "about to insert a new achievement %s", achievement
        achievement_id = achievements.insert(achievement)
    except pymongo.errors.OperationFailure:
        print "oops, mongo error"
        return None
    return achievement_id


def reject_challenge(connection, username, challenge):
    db = connection.achievements_of_life
    try:
        challenge_id = bson.objectid.ObjectId(challenge)
    except TypeError, bson.errors.InvalidId:
        print "bad sessionid passed in"
        return False
    db.users.update({'_id': username}, {'$pull': {'challenges': challenge_id}})
    return True


def add_challenge_to_me(connection, username, challenge):
    db = connection.achievements_of_life
    try:
        challenge_id = bson.objectid.ObjectId(challenge)
    except TypeError, bson.errors.InvalidId:
        print "bad sessionid passed in"
        return False

    if db.users.find(
        {'_id': username, '$or': [{'challenges': challenge_id}, {'achievements': challenge_id}]}).count() > 0:
        print "challange already accepted"
        return False

    db.users.update({'_id': username}, {'$push': {'challenges': challenge_id}})
    return True


def add_challenge_to_friend(connection, username, my_username, challenge):
    db = connection.achievements_of_life
    try:
        challenge_id = bson.objectid.ObjectId(challenge)
    except TypeError, bson.errors.InvalidId:
        print "bad sessionid passed in"
        return False
    achievement_link = {'achievement': challenge_id, 'from': my_username}
    db.users.update({'_id': username}, {'$push': {'challanges_requests_from_friends': achievement_link}})
    return True