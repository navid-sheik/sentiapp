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

