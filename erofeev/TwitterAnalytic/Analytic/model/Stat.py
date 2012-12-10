__author__ = 'erofeev'


class Stat:
    def calc(self, tweets):
        res = {}
        res['manual_happy'] = 0
        res['manual_negative'] = 0
        res['manual_neutral'] = 0
        res['manual_spam'] = 0
        res['auto_happy'] = 0
        res['auto_negative'] = 0
        res['auto_neutral'] = 0
        res['auto_spam'] = 0
        res['total'] = 0
        res['happy'] = 0
        res['negative'] = 0
        res['neutral'] = 0
        res['spam'] = 0

        for tweet in tweets:
            type = ""
            if tweet.isManual:
                type = "manual"
            else:
                type = "auto"
            res[type + "_" + tweet.happiness] += 1
            res[tweet.happiness] += 1
            res['total'] += 1

        for status in {"happy", "negative", "neutral", "spam"}:
            res[status] = int(res[status] / float(res["total"]) * 100) / float(100)
        return res
