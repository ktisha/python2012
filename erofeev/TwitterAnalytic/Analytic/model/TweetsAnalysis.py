#coding: utf-8

from Analytic.model.TwitterStuff import TwitterStuff

__author__ = 'erofeev'
import pymongo

class PredictedTweet:
    """
    Структура для хранения твитта и служебной информации
     """
    text = None
    happiness = None
    isManual = None
    id = None

    def __init__(self, text, happiness, isManual, id):
        self.text = text
        self.happiness = happiness
        self.isManual = isManual
        self.id = id


class TweetsAnalysis:
    """
    Работа с обнаружением настроения твиттов
    """

    @staticmethod
    def predictHappiness(tweets):
        """ для найденных твиттов определяет "настроение" """
        result = []
        for tweet in tweets:
            tweet_id = tweet['id']
            saved = TweetsAnalysis.getSavedResult(tweet_id)
            text = tweet['text']
            if saved is not None:
                result.append(PredictedTweet(text, saved, True, tweet_id))
                return saved
            if 'from_user_id' in tweet:
                userID = tweet['from_user_id']
                #TweetsAnalysis.parseTweet(text)
            happiness = "neutral"
            result.append(PredictedTweet(text, happiness, False, tweet_id))
            #print tweet['from_user_id_str']
        return result

    excuses = ['нет', 'не', 'врятли', 'врядли', 'вряд ли', 'eдва ли', 'навряд ли', 'сомнительно',
               "nope", 'no']


    #TODO убрать спец.символы и обращения (@), оставить хештеги. попробовать сделать морфологию?
    @staticmethod
    def parseTweet(text):
        """ разбивает текст твитта на слова, объединяет слово и предлог-отрицание, убирает спец. символы и т.д. """
        text = text.encode("utf-8")
        for excuse in TweetsAnalysis.excuses:
            try:
                text = text.replace(excuse + " ", "NO")
            except Exception, e:
                pass;
        words = []
        for word in text.split(" "):
            words.append(word)
        return words


    connection_string = "mongodb://localhost"

    @staticmethod
    def getSavedResult(id):
        connection = pymongo.Connection(TweetsAnalysis.connection_string, safe=True)
        results = connection.twitterAnalytic.results
        print results.find_one({"_id": id})
        return


    @staticmethod
    def addTeachedTweets(tweets):
        """ добавляет информацию о вручную определённых твиттах в базу. обновляет индексы для слов """
        print tweets
        connection = pymongo.Connection(TweetsAnalysis.connection_string, safe=True)
        results = connection.twitterAnalytic.results
        for post in tweets:
            if results.find_one("_id") is not None:
                continue
            tweet = TwitterStuff.getTweet(post)
            words = TweetsAnalysis.parseTweet(tweet['text'])
            results.save({"_id": int(post), "happy": tweets[post]})
            for word in words:
                print word