from django.shortcuts import render
from tweets.twitter import Initialize,TwitterClient
from django.views.decorators.csrf import csrf_exempt
import tweets.sentiment_mod
from django.http import JsonResponse
import json
import jsonify
from .models import *
# Create your views here.
@csrf_exempt
def index(request):
    handles = ['@coinmarketcal',
                '@dareandconquer',
                # '@officialmcafee',
                # '@crypt0fungus',
                # '@CryptoMoriarty',
                # '@JonhaRichman',
                # '@CryptoniteTweet',
                # '@crypto_david_',
                # '@alistairmilne',
                # '@bgarlinghouse',
                # '@crypto_null',
                # '@jebus911',
                '@RNR_0',
                '@Cryptopathic']
    api = TwitterClient()
    for name in handles:
        fetch_tweets = api.get_tweets_other(name=name, count=2)
        Initialize.test_tweets_start.clear()
        Initialize.test_tweets_start.extend(fetch_tweets)
        tweets.sentiment_mod.sentiment_list.clear()
        analyzed = tweets.sentiment_mod.main()
        for get_tweets in analyzed:
            tweet = Tweets(twitter_handle=name, tweets = get_tweets, sentiment = analyzed[get_tweets])
            tweet.save()
    result = Tweets.objects.order_by("twitter_handle").values('twitter_handle','tweets','sentiment').distinct()
    print(result)
    return render(request, "index.html",{"result": result})