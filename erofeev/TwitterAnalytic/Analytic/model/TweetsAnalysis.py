#coding: utf-8

from Analytic.model.TwitterStuff import TwitterStuff

__author__ = 'erofeev'
import pymongo
import string


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
        connection = pymongo.Connection(TweetsAnalysis.connection_string, safe=True)
        tweetsColl = connection.twitterAnalytic.tweetsColl
        wordsColl = connection.twitterAnalytic.wordsColl
        for tweet in tweets:
            tweet_id = tweet['id']
            saved = tweetsColl.find_one({"_id": tweet_id})
            text = tweet['text']
            if saved is not None:
                result.append(PredictedTweet(text, saved['happy'], True, tweet_id))
                continue
            if 'from_user_id' in tweet:
                userID = tweet['from_user_id']
                #TweetsAnalysis.parseTweet(text)
            happiness = TweetsAnalysis.predict(text, wordsColl)
            result.append(PredictedTweet(text, happiness, False, tweet_id))
            #print tweet['from_user_id_str']
        return result


    @staticmethod
    def predict(text, wordsColl):
        print text
        words = TweetsAnalysis.parseTweet(text)
        explains = []
        for word in words:
            explain = wordsColl.find_one({"_id": word})
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


    @staticmethod
    def bestVariant(wordStatus):
        i = 0
        bestRate = -1
        best = -1
        states = {"happy", "neutral", "negative", "spam"}
        print wordStatus
        for state in states:
            rate = wordStatus[state] / float(wordStatus["number"])
            print state, rate
            if rate > bestRate:
                best = i
                bestRate = rate
                i += 1
        return (best, bestRate)

    excuses = ['нет', 'не', 'врятли', 'врядли', 'вряд ли', 'eдва ли', 'навряд ли', 'сомнительно',
               "nope", 'no']

    @staticmethod
    def parseTweet(text):
        """ разбивает текст твитта на слова, объединяет слово и предлог-отрицание, убирает спец. символы и т.д. """
        text = text.encode("utf-8")
        for excuse in TweetsAnalysis.excuses:
            try:
                text = text.replace(excuse + " ", "NO")
            except Exception, e:
                pass;
        text = text.replace(",", " ")
        text = text.replace("«", "")
        text = text.replace("»", "")
        words = []
        text = text.translate(string.maketrans("", ""), string.punctuation)
        text = text.translate(string.maketrans("", ""), string.digits)
        for word in text.split(" "):
            if len(word) < 2:
                continue
            word = word.replace(" ", "")
            word = word.decode('utf-8').lower()
            words.append(word)
        return TweetsAnalysis.addPhrases(words)

    @staticmethod
    def addPhrases(words):
        phr = ""
        i = 0
        res = []
        for word in words:
            phr += " " + word
            if i % 2 == 0:
                if len(phr) > 5:
                    res.append(phr[1:])
                phr = ""
            i += 1
        i = 0
        phr = ""
        for word in words[1:]:
            phr += " " + word
            if i % 2 == 0:
                if len(phr) > 5:
                    res.append(phr[1:])
                phr = ""
            i += 1
        res.extend(words)
        return res

    connection_string = "mongodb://localhost"


    @staticmethod
    def addTeachedTweets(tweets):
        """ добавляет информацию о вручную определённых твиттах в базу. обновляет индексы для слов """
        connection = pymongo.Connection(TweetsAnalysis.connection_string, safe=True)
        tweetsColl = connection.twitterAnalytic.tweetsColl
        wordsColl = connection.twitterAnalytic.wordsColl
        for post in tweets:
            if tweetsColl.find_one({"_id": int(post)}) is not None:
                continue
            tweet = TwitterStuff.getTweet(post)
            words = TweetsAnalysis.parseTweet(tweet['text'])

            words.append(tweet['user']['screen_name'])
            tweetsColl.save({"_id": int(post), "happy": tweets[post]})
            for word in words:
                if len(word) < 4:
                    continue
                TweetsAnalysis.saveWord(wordsColl, word, tweets[post])


    @staticmethod
    def saveWord(wordsColl, word, happy):
        savedW = wordsColl.find_one({"_id": word})
        if savedW is None:
            savedW = dict({"_id": word, "happy": 0, "neutral": 0, "negative": 0, "spam": 0, "number": 0})
        savedW[happy] += 1
        savedW["number"] += 1
        wordsColl.save(savedW)


