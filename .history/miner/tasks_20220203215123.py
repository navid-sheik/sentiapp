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
from operator import attrgetter

# import twitter_credentials
nltk.download('vader_lexicon')
nltk.download('stopwords')
ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET =  "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY =  "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"


channel_layer  =  get_channel_layer()
import miner.routing
import json
# @shared_task
# def get_joke ():
#     url  =  'https://api.chucknorris.io/jokes/random'
#     response =  requests.get(url).json()
#     joke  =  response['value']
#     print(joke)
#     print(miner.routing.websocket_urlpatterns)
#     async_to_sync(channel_layer.group_send)('stock', {'type': 'send_joke', 'message' :  joke}) 


@shared_task
def get_stock_info ():

    # url  =  'https://cloud.iexapis.com/stable/stock/tsla/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    url  =  'https://cloud.iexapis.com/stable/stock/tsla/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'
    response =  requests.get(url).json()
    joke  =  response
    print(joke)

    print(miner.routing.websocket_urlpatterns)
    async_to_sync(channel_layer.group_send)('stock', {'type': 'send_joke', 'message' :  joke}) 



# def get_history_data():
#     url  =  "https://cloud.iexapis.com/stable/stock/tsla/chart/max?token=pk_8295cd8fa9064272b2335b548a28d293"
#     response =  requests.get(url).json()

#     input_dict = json.loads(response)
    

#     async_to_sync(channel_layer.group_send)('stock', {'type': 'send_joke', 'message' :  joke}) 



@shared_task(bind=True)
def mineTweets (self, ticker):
  

    dict  = {"tsla" : "#TSLA #tsla tsla TSLA"}
    auth =  OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets  =  100
    tweets  =  []
    likes = []
    time = []
    keyword  = dict[ticker]
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
        stockSummary = StockSummary.objects.get(ticker=ticker)
    except StockSummary.DoesNotExist:
        stockSummary  =  StockSummary(ticker=ticker, last_fetched = datetime.datetime.now())
        stockSummary.save()
    for tweet in cursor:
        if 'retweeted_status' in tweet._json:
                full_text_tweet  =  tweet._json['retweeted_status']['full_text']
        else:
                full_text_tweet = tweet.full_text

    
        map_sentimet=  perfomSentimentAnalysis(cleanTweet(full_text_tweet))
        print("The negative value is  ",  map_sentimet['neg'])
        

        try:
            tweet_record = TweetRecord.objects.get(tweet_id=tweet.id_str)
        except TweetRecord.DoesNotExist:
            tweet_record = TweetRecord(
                stock=stockSummary, 
                tweet_id=tweet.id_str,
                tweet_date =  tweet.created_at ,
                raw_text =  full_text_tweet ,
                processed_text =  cleanTweet(full_text_tweet),
                stemmed_text =  clean_text(cleanTweet(full_text_tweet)),
                polarity =   TextBlob(cleanTweet(full_text_tweet)).sentiment.polarity,
                sentiment =  map_sentimet['text_sentiment'],
                subjectivity =  TextBlob(cleanTweet(full_text_tweet)).sentiment.subjectivity,
                neg =  map_sentimet['neg'],
                neu =  map_sentimet['neu'],
                pos =  map_sentimet['pos'],
                compound  = map_sentimet['comp'],
                retweet = tweet.retweet_count,
                likes =  tweet.favorite_count,
            )
            tweet_record.save()


@shared_task(bind=True)
def createHourlyRecord (self,ticker):
    print("Ticker" + ticker)
    #have only 24 hours record for each , then overwritte

    
    stock =  get_object_or_404(StockSummary, ticker = ticker)
    current_date  =  datetime.datetime.now()
    # current_hour =  datetime.datetime.now().time().hour
    created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    list_records_previous_day =  TweetRecord.objects.filter(stock = stock,tweet_date__lte= created_time)



    #Negative/ positivite/ negative 
    count_negative = 0
    count_neutral= 0
    count_positive = 0

    tweet_negative_list = []
    tweet_positive_list = []
    tweet_neutral_list = []

   
   

    for tweet in list_records_previous_day:
        if tweet.neg > tweet.pos:
            tweet_negative_list.append(tweet)
            count_negative += 1
        elif tweet.pos > tweet.neg:
            tweet_positive_list.append(tweet)
            count_positive += 1
        elif tweet.pos == tweet.neg:
            tweet_neutral_list.append(tweet)
            count_neutral += 1


    most_positive  =  getMostInfluentialTweet(tweet_positive_list)
    most_negative=   getMostInfluentialTweet(tweet_negative_list)
    most_neutral=  getMostInfluentialTweet(tweet_neutral_list)
    most_polarity=   list_records_previous_day.order_by('-polarity').first().tweet_id
    most_subjectivity=   list_records_previous_day.order_by('-subjectivity').first().tweet_id

    #Create list of stemmed word 
    list_stemmed=  list_records_previous_day.values_list('stemmed_text', flat=True)
 
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
        overall_stemmed_text = stemmed_text_compress(list_stemmed),
        overall_neg =  mean_negative,
        overall_neu =  mean_neutrality,
        overall_pos =  mean_positive,
        overall_compound =  mean_compound,
        negative_count = count_negative,
        positive_count =  count_positive,
        neutraul_count =  count_neutral

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


def stemmed_text_compress(list):
    mytext  =  " "
    for obj in list:
        mytext += obj + " "
    return mytext

stopword = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text

#Cleaning Text
def clean_text(text):
    text_lc = "".join([word.lower() for word in text if word not in string.punctuation]) # remove puntuation
    text_rc = re.sub('[0-9]+', '', text_lc)
    tokens = re.split('\W+', text_rc)    # tokenization
    # text = [ps.stem(word) for word in tokens if word not in stopword]  # remove stopwords and stemming
    text =  [ word.lower() for word in tokens if word not in stopword]

    text_values  =   ' '.join(text)

    return text_values

def getMostInfluentialTweet(tweet_list):

    max_obj  = max(tweet_list, key=attrgetter('favorite_count'))
    tweet_id_to_return =  max_obj.tweet.id_str
  
    return tweet_id_to_return
