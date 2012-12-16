#coding: utf-8

from Analytic.model.Parser import Parser
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
    tweetsColl = None
    wordsColl = None

    def __init__(self):
        connection = pymongo.Connection(TweetsAnalysis.connection_string, safe=True)
        self.tweetsColl = connection.twitterAnalytic.tweetsColl
        self.wordsColl = connection.twitterAnalytic.wordsColl


    def predictHappiness(self, tweets):
        """ для найденных твиттов определяет "настроение" """
        result = []
        for tweet in tweets:
            tweet_id = tweet['id']
            saved = self.tweetsColl.find_one({"_id": tweet_id})
            text = tweet['text']
            if saved is not None:
                result.append(PredictedTweet(text, saved['happy'], True, tweet_id))
                continue
            happiness = self.predict(text, "@" + tweet['from_user'])
            result.append(PredictedTweet(text, happiness, False, tweet_id))
            #print tweet['from_user_id_str']
        return result

    def predict(self, text, user):
        words = Parser().parseTweet(text)
        words.append(user)
        explains = []
        for word in words:
            explain = self.wordsColl.find_one({"_id": word})
            if explain is None:
                continue
            explains.append(explain)
        explains.sort(lambda x1, x2: x1["number"] - x2["number"])
        explains.reverse()
        res = dict({"happy": 0, "neutral": 0, "negative": 0, "spam": 0})
        states = {"happy", "neutral", "negative", "spam"}
        for explain in explains:
            n = explain["number"] / float(explains[0]["number"])
            for state in states:
                res[state] += explain[state] * n
        best = ""
        bestRate = -1
        for state in states:
            if res[state] > bestRate:
                bestRate = res[state]
                best = state
        return best

    connection_string = "mongodb://localhost"


    def addTeachedTweets(self, tweets):
        """ добавляет информацию о вручную определённых твиттах в базу. обновляет индексы для слов """
        for tweetId in tweets:
            if self.tweetsColl.find_one({"_id": int(tweetId)}) is not None:
                continue
            tweet = TwitterStuff.getTweet(tweetId)
            if tweet is None:
                continue
            words = Parser().parseTweet(tweet['text'])
            words.append("@" + tweet['user']['screen_name'])
            self.tweetsColl.save({"_id": int(tweetId), "happy": tweets[tweetId]})
            for word in words:
                if len(word) < 4:
                    continue
                self.saveWord(word, tweets[tweetId])


    def saveWord(self, word, happy):
        savedW = self.wordsColl.find_one({"_id": word})
        if savedW is None:
            savedW = dict({"_id": word, "happy": 0, "neutral": 0, "negative": 0, "spam": 0, "number": 0})
        savedW[happy] += 1
        savedW["number"] += 1
        self.wordsColl.save(savedW)


