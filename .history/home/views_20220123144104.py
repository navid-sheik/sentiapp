from distutils.command import clean
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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from .models import HourlyRecord, StockSummary, TweetRecord
import datetime
import statistics

from statistics import mode

from collections import Counter


from .tasks import test_func

# import twitter_credentials
nltk.download('vader_lexicon')
nltk.download('stopwords')



ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET =  "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY =  "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"

def index(request):
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
        # if 'retweeted_status' in tweet._json:
        #     print("THIS IS A RETWEEN")
        #     print(tweet._json['retweeted_status']['full_text'])
        # else:
        #     print(tweet.full_text)
        # print(tweet.full_text)
        # print(cleanTweet(tweet.full_text))
        # print(tweet.id_str)
        # print(tweet.created_at)
        if 'retweeted_status' in tweet._json:
            map_sentimet=  perfomSentimentAnalysis(cleanTweet(tweet._json['retweeted_status']['full_text']))
        else:
            map_sentimet=  perfomSentimentAnalysis(cleanTweet(tweet.full_text))
        # print("The negative value is  ",  map_sentimet['neg'])
        
        if 'retweeted_status' in tweet._json:
                tweetToInput  =  tweet._json['retweeted_status']['full_text']
        else:
                tweetToInput = tweet.full_text

        try:
            tweet_record = TweetRecord.objects.get(tweet_id=tweet.id_str)
        except TweetRecord.DoesNotExist:
           
            tweet_record = TweetRecord(
                stock=stockSummary, 
                tweet_id=tweet.id_str,
                tweet_date =  tweet.created_at ,
                raw_text =  tweetToInput,
                processed_text =  cleanTweet(tweetToInput),
                stemmed_text =  clean_text(cleanTweet(tweetToInput)),
                polarity =   TextBlob(cleanTweet(tweetToInput)).sentiment.polarity,
                sentiment =  map_sentimet['text_sentiment'],
                subjectivity =  TextBlob(cleanTweet(tweetToInput)).sentiment.subjectivity,
                neg =  map_sentimet['neg'],
                neu =  map_sentimet['neu'],
                pos =  map_sentimet['pos'],
                compound  = map_sentimet['comp']
            )
            tweet_record.save()


       
     

        tweet_list.append(tweetToInput)
        analysis = TextBlob(tweetToInput)
        score = SentimentIntensityAnalyzer().polarity_scores(tweetToInput)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity
        
        if neg > pos:
            negative_list.append(tweetToInput)
            negative += 1
        elif pos > neg:
            positive_list.append(tweetToInput)
            positive += 1
        
        elif pos == neg:
            neutral_list.append(tweetToInput)
            neutral += 1

    # positive = percentage(positive, number_of_tweets)
    # negative = percentage(negative, number_of_tweets)
    # neutral = percentage(neutral, number_of_tweets)
    # polarity = percentage(polarity, number_of_tweets)
    # positive = format(positive, '.1f')
    # negative = format(negative, '.1f')
    # neutral = format(neutral, '.1f')


    #Number of Tweets (Total, Positive, Negative, Neutral)
    # print("Before " +  str(len(tweet_list)))
    tweet_list = list(dict.fromkeys(tweet_list))
    # print("AFter " +   str(len(tweet_list)))


    
    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    # print('total number: ',len(tweet_list))
    # print('positive number: ',len(positive_list))
    # print('negative number: ', len(negative_list))
    # print('neutral number: ',len(neutral_list))

    # print(tweet_list)

    # tweet_list.drop_duplicates(inplace = True)


 


    tw_list = pd.DataFrame(tweet_list)
    tw_list["text"] = tw_list[0]

    #Removing RT, Punctuation etc
    remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
    rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] =tw_list.text.str.lower()
  
    # print(tw_list.head(100))


    # tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    # for index, row in tw_list['text'].iteritems():
    #     score = SentimentIntensityAnalyzer().polarity_scores(row)
    #     neg = score['neg']
    #     neu = score['neu']
    #     pos = score['pos']
    #     comp = score['compound']
    #     if neg > pos:
    #         tw_list.loc[index, 'sentiment'] = "negative"
    #     elif pos > neg:
    #         tw_list.loc[index, 'sentiment'] = "positive"
    #     else:
    #         tw_list.loc[index, 'sentiment'] = "neutral"
    #     tw_list.loc[index, 'neg'] = neg
    #     tw_list.loc[index, 'neu'] = neu
    #     tw_list.loc[index, 'pos'] = pos
    #     tw_list.loc[index, 'compound'] = comp

 
    createHourlyRecord('TSL')

    context = {"tweets" : tw_list.to_html(), "navid" : "something"}
    return render(request, 'home/pages/home.html', context)


def get_tweets(ticker):
    return


def dropDuplicates (tweet_list):
    return

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

def mean(list_sentiment):
    return statistics.mean(list_sentiment) 

def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)

#run every hour
def createHourlyRecord(ticker):
    #have only 24 hours record for each , then overwritte
    stock =  get_object_or_404(StockSummary, ticker = ticker)
    current_date  =  datetime.datetime.now()
    current_hour =  datetime.datetime.now().time().hour
    list_records_previous_day =  TweetRecord.objects.filter(stock = stock,tweet_date__hour=(current_hour))
    #Create hourly record
    # list_stemmed=  list_records_previous_day.values('stemmed_text', flat=True)
    # print(list_stemmed)

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


#run at midnight
def createDailyRecord(ticker):
    #daily record of each day
    stock =  get_object_or_404(StockSummary, ticker = ticker)

    previous_day =  datetime.date.today()-datetime.timedelta(1)
    list_records_previous_day =  TweetRecord.objects.filter(stock = stock,tweet_date__range=[datetime.date.today(), datetime.timedelta(1)])
    #Create hourly record

    return



#run at midnight every month, 1st
def createMonthlyRecord(ticker):
    stock =  get_object_or_404(StockSummary, ticker = ticker)
    month = datetime.datetime.today().month
    list_records_previous_month =  TweetRecord.objects.filter(stock = stock,tweet_date__month = month)
    return


def test(request):
    #test_func.delay()
    return HttpResponse("Done")




#Appliyng tokenization
def tokenization(text):
    text = re.split('\W+', text)
    return text



stopword = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text


#Appliyng Stemmer
ps = nltk.PorterStemmer()
def stemming(text):
    text = [ps.stem(word) for word in text]
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