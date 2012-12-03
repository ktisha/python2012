import simplejson
import urllib2

__author__ = 'erofeev'

class TwitterStuff:
    """
    Работа с твиттером
     """

    @staticmethod
    def getTweets(query, tweetsN, result_type):
        query = urllib2.quote(query.encode("utf-8"))
        url = "http://search.twitter.com/search.json?q=" + query + "&rpp=" + str(
            tweetsN) + "&result_type=" + result_type
        try:
            f = urllib2.urlopen(url)
            tweets = simplejson.load(f)
            return tweets['results']
        except urllib2.HTTPError:
            return None

    @staticmethod
    def getTweet(id):
        try:
            f = urllib2.urlopen("https://api.twitter.com/1/statuses/show.json?id=" + id)
            return simplejson.load(f)
        except urllib2.HTTPError:
            return None
