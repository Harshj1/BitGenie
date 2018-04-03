import re
import tweepy
from tweepy import OAuthHandler
#from textblob import TextBlob
from tweets.sentiment_mod import Initialize
import tweets.sentiment_mod


class TwitterClient(object):
    def __init__(self):

        consumer_key = 'ML1OP1Oxe81AZjXrp6UYHXb14'
        consumer_secret = 'eEeOyMuzsi7TkAtmo1tFXrAusNLBxVYQClYw9DP4DNe5RUEgDH'
        access_token = '830480924479401984-wERHiXXjoDH0vDY2jvEfl31VC6wWR0s'
        access_token_secret = 'CrSChUizox55tDlZz5f6AOmYgRGxmljDAfLws5aWKPYMX'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweets_other(self, count=10, name=''):
        tweets = []
        try:
            fetched_tweets = self.api.user_timeline(id=name, count=count, tweet_mode='extended')
            for tweet in fetched_tweets:
                tweets.append(self.clean_tweet(tweet.full_text))
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))
