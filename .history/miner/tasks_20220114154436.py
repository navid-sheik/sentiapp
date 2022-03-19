from celery import shared_task

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import langdetect

# Create your views here.
from tweepy  import Stream, auth
from tweepy import OAuthHandler
import tweepy
from home.models import HourlyRecord, StockSummary, TweetRecord
import datetime

ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET =  "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY =  "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"


@shared_task(bind=True)
def test_func2 (self):


    auth =  OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets  =  100
    tweets  =  []
    likes = []
    time = []
    keyword  = 'Tesla #tesla'
    cursor  =  tweepy.Cursor(api.search_tweets, q= keyword, tweet_mode="extended", lang="en").items(number_of_tweets)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    try:
        stockSummary = StockSummary.objects.get(ticker="TSL")
    except StockSummary.DoesNotExist:
        stockSummary  =  StockSummary(ticker="TSL", last_fetched = datetime.datetime.now())
        stockSummary.save()
    for i in range(10):
        print(i)
    return "Done"