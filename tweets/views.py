from django.shortcuts import render
from tweets.twitter import Initialize,TwitterClient
from django.views.decorators.csrf import csrf_exempt
import tweets.sentiment_mod
from django.http import JsonResponse
import json
import jsonify
# Create your views here.
@csrf_exempt
def index(request):
    handles = ['']
    api = TwitterClient()
    req_data = json.loads(request.body)
    choice = req_data['choice']
    user_param = req_data['user_param']
    print(user_param)
    print(choice)
    if (choice == 1):  # self timeline
        tweets = api.get_tweets_self(count=10)
        Initialize.test_tweets_start.extend(tweets)
        # print(Initialize.test_tweets_start)
        analyzed = tweets.sentiment_mod.main()

        return JsonResponse(analyzed,safe=False)
    elif (choice == 2):  # other timeline
        tweets = api.get_tweets_other(name=user_param, count=10)
        Initialize.test_tweets_start.extend(tweets)
        # print(Initialize.test_tweets_start)
        analyzed = tweets.sentiment_mod.main()
        return JsonResponse(analyzed,safe=False)

    else:  # trends
        trends = api.get_trends()
        print(trends)
        return JsonResponse(trends,safe=False)