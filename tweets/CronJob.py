from django_cron import CronJobBase, Schedule
from tweets.twitter import Initialize,TwitterClient
import tweets.sentiment_mod
from .models import *

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tweets.my_cron_job'    # a unique code

    def do(self):
        handles = ['@coinmarketcal',
                   '@dareandconquer',
                   '@officialmcafee',
                   '@crypt0fungus',
                   '@CryptoMoriarty',
                   '@JonhaRichman',
                   '@CryptoniteTweet',
                   '@crypto_david_',
                   '@alistairmilne',
                   '@bgarlinghouse',
                   '@crypto_null',
                   '@jebus911',
                   '@RNR_0',
                   '@Cryptopathic']
        api = TwitterClient()
        for name in handles:
            fetch_tweets = api.get_tweets_other(name=name, count=2)
            Initialize.test_tweets_start.clear()
            Initialize.test_tweets_start.extend(fetch_tweets)
            analyzed = tweets.sentiment_mod.main()
            for get_tweets in analyzed:
                tweet = Tweets(twitter_handle=name, tweets=get_tweets, sentiment=analyzed[get_tweets])
                tweet.save()