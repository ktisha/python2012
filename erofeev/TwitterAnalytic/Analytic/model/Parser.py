#coding: utf-8

__author__ = 'erofeev'
import string

class Parser:
    excuses = ['нет', 'не', 'врятли', 'врядли', 'вряд ли', 'eдва ли', 'навряд ли', 'сомнительно',
               "nope", 'no', "редко"]

    def parseTweet(self, text):
        """ разбивает текст твитта на слова, объединяет слово и предлог-отрицание, убирает спец. символы и т.д. """
        text = text.encode("utf-8")
        print "start parse"
        for excuse in self.excuses:
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
        return self.addPhrases(words)

    def addPhrases(self, words):
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
