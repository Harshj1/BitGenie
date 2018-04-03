from django.db import models

# Create your models here.

class Tweets(models.Model):
    tweet_id = models.AutoField(primary_key=True)
    twitter_handle = models.CharField(max_length=100)
    tweets = models.CharField(max_length=300)
    sentiment = models.CharField(max_length=50)

    def __str__(self):  # __unicode__ on Python 2
        string = self.twitter_handle + str(self.tweet_id)
        return string
