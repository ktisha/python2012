#coding: utf-8
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from Analytic.model.TwitterStuff import TwitterStuff
from Analytic.model.TweetsAnalysis import TweetsAnalysis
from Analytic.model.Stat import Stat

def search(request):
    """Страница ввода данных для поиска"""

    params = {}
    if request.GET.get('error', '') is not None:
        error = request.GET.get('error', '')
        if error == "bad_n":
            params['error'] = 'Плохое количество твиттов'
        elif error == "bad_q":
            params['error'] = 'Плохой запрос'
        elif error == "many_t":
            params['error'] = 'Слишком много твиттов'
        else:
            params["error"] = error
    return  render(request, 'search.html', params)


def result(request):
    """Страница отрисовки твиттов с настроениями"""

    query = request.GET.get('q', '')
    tweetsStr = request.GET.get('rpp', '')
    result_type = request.GET.get('result_type', '')
    if query is None or len(query) == 0:
        return redirect("/search?error=bad_q")
    try:
        tweetsN = int(tweetsStr)
        if tweetsN > 100:
            return redirect("/search?error=many_t")
    except:
        #return redirect("/search?error=bad_n")
        tweetsN = 20

    result = {}
    tweets = TweetsAnalysis().predictHappiness(TwitterStuff.getTweets(query, tweetsN, result_type))
    result['tweets'] = tweets
    result['stat'] = Stat().calc(tweets)
    print result['stat']
    result['query'] = query
    return render(request, 'result.html', result)


@csrf_exempt
def recipient(request):
    """Ассинхронный приём новой информации от "учителя" о настроениях """
    TweetsAnalysis().addTeachedTweets(request.POST)
    return HttpResponse("OK")
