import imp
from urllib import request
from celery import shared_task

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import langdetect

# Create your views here.
from tweepy  import Stream, auth
from tweepy import OAuthHandler
import tweepy

from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
# from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from home.models import HourlyRecord, StockSummary, TweetRecord
import datetime
import statistics

from statistics import mode

from collections import Counter
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# import twitter_credentials
nltk.download('vader_lexicon')

ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET =  "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY =  "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"


channel_layer  =  get_channel_layer()

@shared_task
def get_joke ():
    url  =  'https://api.chucknorris.io/jokes/random'
    response =  requests.get(url).json()
    joke  =  response['value']
    
    async_to_sync(channel_layer.group_send)('stock', {'type': 'send_jokes', 'message' :  joke}) 



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
    for tweet in cursor:
        print(tweet.full_text)
        print(cleanTweet(tweet.full_text))
        print(tweet.id_str)
        print(tweet.created_at)
        map_sentimet=  perfomSentimentAnalysis(cleanTweet(tweet.full_text))
        print("The negative value is  ",  map_sentimet['neg'])
        

        try:
            tweet_record = TweetRecord.objects.get(tweet_id=tweet.id_str)
        except TweetRecord.DoesNotExist:
            tweet_record = TweetRecord(
                stock=stockSummary, 
                tweet_id=tweet.id_str,
                tweet_date =  tweet.created_at ,
                raw_text =  tweet.full_text ,
                processed_text =  cleanTweet(tweet.full_text),
                polarity =   TextBlob(cleanTweet(tweet.full_text)).sentiment.polarity,
                sentiment =  map_sentimet['text_sentiment'],
                subjectivity =  TextBlob(cleanTweet(tweet.full_text)).sentiment.subjectivity,
                neg =  map_sentimet['neg'],
                neu =  map_sentimet['neu'],
                pos =  map_sentimet['pos'],
                compound  = map_sentimet['comp']
            )
            tweet_record.save()


@shared_task(bind=True)
def createHourlyRecord (self,ticker):
    print("Ticker" + ticker)
    #have only 24 hours record for each , then overwritte
    stock =  get_object_or_404(StockSummary, ticker = ticker)
    current_date  =  datetime.datetime.now()
    current_hour =  datetime.datetime.now().time().hour
    list_records_previous_day =  TweetRecord.objects.filter(stock = stock,tweet_date__hour=(current_hour))
    #Create hourly record
    list_subjectivity =  list_records_previous_day.values_list('subjectivity', flat=True)
    mean_subjectivity =  round(mean(list_subjectivity), 6)


    list_polarity =  list_records_previous_day.values_list('polarity', flat=True)
    mean_polarity =  round(mean(list_polarity), 6)


    list_negative=  list_records_previous_day.values_list('neg', flat=True)
    mean_negative =  round(mean(list_negative), 3)

    list_neutrality =  list_records_previous_day.values_list('neu', flat=True)
    mean_neutrality =  round(mean(list_neutrality), 3)

    list_positivity =  list_records_previous_day.values_list('pos', flat=True)
    mean_positive=  round(mean(list_positivity), 3)

    list_compound =  list_records_previous_day.values_list('compound', flat=True)
    mean_compound =  round(mean(list_compound), 4)


    #to evaluate 
    list_sentiment=  list_records_previous_day.values_list('sentiment', flat=True)
    most_common =  mode(list_sentiment)

    print(list_sentiment)

    hourly, created =  HourlyRecord.objects.update_or_create(
        stock =  stock,
        tweet_date =  current_date,
        overall_polarity =  mean_polarity,
        overall_sentiment =  most_common,
        overall_subjectivity =  mean_subjectivity,
        overall_neg =  mean_negative,
        overall_neu =  mean_neutrality,
        overall_pos =  mean_positive,
        overall_compound =  mean_compound

    )
    if created == True:
        print("Successfucl")



def mean(list_sentiment):
    return statistics.mean(list_sentiment) 


def perfomSentimentAnalysis (tweet):
    tweet_sentiment  =  TextBlob(tweet).sentiment
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    sentiment_text  = ""
    if neg > pos:
        sentiment_text = "negative"
    elif pos > neg:
        sentiment_text = "positive"
    else:
        sentiment_text =  "neutral"

    sentiment  = {}
    sentiment["neg"] = neg
    sentiment["neu"] = neu
    sentiment["pos"] = pos
    sentiment["comp"] = comp
    sentiment["text_sentiment"] = sentiment_text

    return sentiment

def cleanTweet(tweet):
     
  

    #remove placeholder video 
    # new_tweet =  re.sub(r'{link}', '', tweet)

    # new_tweet = re.sub(r"\[video\]", '', new_tweet)

    # #not letter , punction , emoji , hash , non  english 
    # new_tweet =  re.sub(r"[^a-z\s\(\-:\)\\\/\];='#]", '', new_tweet)


    #twitter mention 
    new_tweet =  re.sub(r'@mention', '', tweet)


    # it will remove the old style retweet text "RT"
    new_tweet = re.sub(r'^RT[\s]+', '', new_tweet)

    # it will remove hyperlinks
    new_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', new_tweet)

    # it will remove hashtags. We have to be careful here not to remove 
    # the whole hashtag because text of hashtags contains huge information. 
    # only removing the hash # sign from the word
    new_tweet = re.sub(r'#', '', new_tweet)

    # it will remove single numeric terms in the tweet. 
    new_tweet = re.sub(r'[0-9]', '', new_tweet)


    new_tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",new_tweet)
    new_tweet =  new_tweet.lower()
 
    return new_tweet