

import datetime
import imp
import json
import re
import statistics
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from matplotlib.font_manager import json_dump
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
# Create your views here.
from tweepy import Stream, auth
from tweepy import OAuthHandler
import tweepy
from home.models import TweetRecord, HourlyRecord, StockSummary
from datetime import timedelta

ACCESS_TOKEN = "1473341591532326912-WaFVz4x6yxfXeZE3sjge7d6F7sVS4A"

ACCESS_TOKEN_SECRET = "jdAUx7NW90EqxsQwk7eYP6G2JbVwJ8MGAUYwadxZU4axB"

CONSUMER_KEY = "UdSOEJpvWgKUkBIuQbTo4S2kS"

CONSUMER_SECRET = "P0JwU7GIN9gOPZ1zrvjffl9XxrnPYSb3DFpbnlsJbjVsFh8cP3"


def fetchStockData(request, ticker_id):
    stock_ticker = ticker_id.lower()
    url = f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_quote': response})


def fetchCompanyInfo(request, ticker_id):
    stock_ticker = ticker_id.lower()
    url = f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/company?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_quote': response})



def fetchStockDataHistory(request, ticker_id, timestamp):
    stock_ticker = ticker_id.lower()
    url = f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/{timestamp}?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_quote': response})




def get_single_tweet_sentiment(request, sentiment_type,record_id):

    record  =  HourlyRecord.objects.filter(pk=record_id).first()
    tweet_id =  ""
    if sentiment_type == "positive":
        tweet_id  = record.best_tweet_positive
    elif  sentiment_type == "negative":
        tweet_id  = record.best_tweet_negative
        
    elif  sentiment_type == "neutral":
        tweet_id  = record.best_tweet_neutral
    elif  sentiment_type == "subjectivity":
        tweet_id  = record.best_tweet_subjectivity
    elif  sentiment_type == "polarity":
        tweet_id  = record.best_tweet_polarity
    elif  sentiment_type == "compound":
        tweet_id  = record.best_tweet_negative
        
    


    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    tweet = api.get_status(tweet_id)
    print(tweet)
    return JsonResponse({'single_tweet' :  json.dumps(tweet._json)})


def getHotTweet(request):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    number_of_tweets = 100
    keyword = 'Tesla #tesla'
    # keyword  = generateSearchQuery(ticker)
    cursor = tweepy.Cursor(api.search_tweets, q=keyword,
                           tweet_mode="extended", result_type='recent', lang="en").items(1)

    searched_tweets = [status._json for status in cursor]
    json_string = [json.dumps(json_obj) for json_obj in searched_tweets]
    return JsonResponse({'tweet': json_string})


def get_single_tweet(request, tweet_id):

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweet = api.get_status(tweet_id)
    return JsonResponse({'single_tweet' :  json.dumps(tweet)})
 

def getPopularTweets(request, ticker_id):
    stock_ticker =  ticker_id.lower()
    dict  = {"tsla" : "#TSLA #tsla tsla TSLA"}
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets = 20

    # keyword = dict[ticker_id]
    keyword  = generateSearchQuery(stock_ticker)
    cursor = tweepy.Cursor(api.search_tweets, q=keyword,
                           tweet_mode="extended", result_type='popular', lang="en").items(number_of_tweets)

    tweets_sentiments  =  []
    for tweet in cursor:
        if 'retweeted_status' in tweet._json:
                full_text_tweet  =  tweet._json['retweeted_status']['full_text']
        else:
                full_text_tweet = tweet.full_text

    
        map_sentimet=  perfomSentimentAnalysis(cleanTweet(full_text_tweet))
        mytweet  =   tweet._json
        mytweet['sentiment']  =  map_sentimet['text_sentiment']
        tweets_sentiments.append(mytweet)
 
    return JsonResponse({'tweets': json.dumps( tweets_sentiments),
                         
    
    
    })

def getRecentTweets(request, ticker_id):
    stock_ticker =  ticker_id.lower()
    dict  = {"tsla" : "#TSLA #tsla tsla TSLA"}
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    number_of_tweets = 20
    # keyword = dict[ticker_id]
    keyword  = generateSearchQuery(stock_ticker)
    cursor = tweepy.Cursor(api.search_tweets, q=keyword,
                           tweet_mode="extended", result_type='recent', lang="en").items(number_of_tweets)

    tweets_sentiments  =  []
    for tweet in cursor:
        if 'retweeted_status' in tweet._json:
                full_text_tweet  =  tweet._json['retweeted_status']['full_text']
        else:
                full_text_tweet = tweet.full_text

    
        map_sentimet=  perfomSentimentAnalysis(cleanTweet(full_text_tweet))
        mytweet  =   tweet._json
        mytweet['sentiment']  =  map_sentimet['text_sentiment']
        tweets_sentiments.append(mytweet)

    return JsonResponse({'tweets': json.dumps( tweets_sentiments),})


def getSearchTwitter(request, keyword_search):

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    number_of_tweets = 20

    keyword = keyword_search
    
    cursor = tweepy.Cursor(api.search_tweets, q=keyword,
                           tweet_mode="extended", result_type='recent', lang="en").items(number_of_tweets)

    searched_tweets = [status._json for status in cursor]
    return JsonResponse({'tweets': json.dumps( searched_tweets)})


def get_tweets_based_sentiment(request, ticker_id):
    stock_ticker =  ticker_id.lower()
    dict  = {"tsla" : "#TSLA #tsla tsla TSLA"}
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    now = datetime.datetime.today().now()
    prev=now-timedelta(days=1)
    now=now.strftime("%Y-%m-%d")
    prev=prev.strftime("%Y-%m-%d")

    negative_list  =  []
    positive_list =  []
    neutral_list =  []
    
    number_of_tweets = 20

    # keyword = dict[ticker_id]
    keyword  = generateSearchQuery(stock_ticker)
    cursor = tweepy.Cursor(api.search_tweets, q=keyword, since=prev, until=now,
                           tweet_mode="extended", result_type='recent', lang="en").items(number_of_tweets)

    tweets_sentiments  =  []
    for tweet in cursor:
        if 'retweeted_status' in tweet._json:
                full_text_tweet  =  tweet._json['retweeted_status']['full_text']
        else:
                full_text_tweet = tweet.full_text

    
        map_sentimet=  perfomSentimentAnalysis(cleanTweet(full_text_tweet))
        mytweet  =   tweet._json
        if map_sentimet['text_sentiment'] == 'positive':
            positive_list.append(mytweet)

        elif map_sentimet['text_sentiment'] == 'negative':
            negative_list.append(mytweet)
        else:
            neutral_list.append(mytweet)

    return JsonResponse({'negatives': json.dumps( negative_list),
                         'positives' :  json.dumps(positive_list),
                         'neutrals' :   json.dumps(neutral_list)})

def getSentiment24Hours(request, ticker_id):
    stock_ticker =  ticker_id.lower()
    stock = get_object_or_404(StockSummary, ticker= stock_ticker)
    date_from = datetime.datetime.now() - datetime.timedelta(days=2)
    records = HourlyRecord.objects.filter(
    stock=stock, tweet_date__gte=date_from)
    
    list_ids = records.values_list('id', flat=True)
    fetched_date = datetime.datetime.now()
    list_date = records.values_list('tweet_date', flat=True)
    list_stemmed = records.values_list('overall_stemmed_text', flat=True)
    wordcloud = stemmed_text_compress(list_stemmed)

    list_negative_count = records.values_list('negative_count', flat=True)
    negative_count_24_hours = sum(list_negative_count)

    list_positive_count = records.values_list('positive_count', flat=True)
    positive_count_24_hours = sum(list_positive_count)

    list_neutraul_count = records.values_list('neutraul_count', flat=True)
    neutraul_count_24_hours = sum(list_neutraul_count)

    total_tweets_count = negative_count_24_hours + positive_count_24_hours + neutraul_count_24_hours

    list_negative = records.values_list('overall_neg', flat=True)
    mean_negative_24_hours = mean(list_negative)

    list_neutral = records.values_list('overall_neu', flat=True)
    mean_neutral_24_hours = mean(list_neutral)

    list_positive = records.values_list('overall_pos', flat=True)
    mean_positive_24_hours = mean(list_positive)

    list_compound = records.values_list('overall_compound', flat=True)
    mean_compound_24_hours = mean(list_compound)

    list_subjecivity = records.values_list('overall_subjectivity', flat=True)
    mean_subjectivity_24_hours = mean(list_subjecivity)

    list_polarity = records.values_list('overall_polarity', flat=True)
    mean_polarity_24_hours = mean(list_polarity)

    return JsonResponse({  
        'list_ids' : list(list_ids),
        'fetched_date': fetched_date,
        'word_cloud_data': wordcloud,
        'negative_count': negative_count_24_hours,
        'positive_count': positive_count_24_hours,
        'neutral_count': negative_count_24_hours,
        'mean_negative': mean_negative_24_hours,
        'mean_positive':  mean_positive_24_hours,
        'mean_neutral':  mean_neutral_24_hours,
        'mean_polarity': mean_polarity_24_hours,
        'mean_subjectivity':  mean_subjectivity_24_hours,
        'mean_compound':  mean_compound_24_hours,
        'values_negatives':  list(list_negative),
        'values_positives':  list(list_positive),

        'values_neutral':  list(list_neutral),

        'values_compound':  list(list_compound),


        'values_polarity':  list(list_polarity),
        'values_subjectivity':  list(list_subjecivity),
        'dates' :  [dt.date() for dt in list_date]

    })



def getSentimentTimeRange(request, ticker_id, time_range):
    stock_ticker =  ticker_id.lower()
    stock = get_object_or_404(StockSummary, ticker=stock_ticker)
    date_from = datetime.datetime.now() - datetime.timedelta(days=time_range)
    records = HourlyRecord.objects.filter(
        stock=stock, tweet_date__gte=date_from)


    list_ids = records.values_list('id', flat=True)
    fetched_date = datetime.datetime.now()
    list_date = records.values_list('tweet_date', flat=True)
    list_stemmed = records.values_list('overall_stemmed_text', flat=True)
    wordcloud = stemmed_text_compress(list_stemmed)

    list_negative_count = records.values_list('negative_count', flat=True)
    negative_count_24_hours = sum(list_negative_count)

    list_positive_count = records.values_list('positive_count', flat=True)
    positive_count_24_hours = sum(list_positive_count)

    list_neutraul_count = records.values_list('neutraul_count', flat=True)
    neutraul_count_24_hours = sum(list_neutraul_count)

    total_tweets_count = negative_count_24_hours + positive_count_24_hours + neutraul_count_24_hours

    list_negative = records.values_list('overall_neg', flat=True)
    mean_negative_24_hours = mean(list_negative)

    list_neutral = records.values_list('overall_neu', flat=True)
    mean_neutral_24_hours = mean(list_neutral)

    list_positive = records.values_list('overall_pos', flat=True)
    mean_positive_24_hours = mean(list_positive)

    list_compound = records.values_list('overall_compound', flat=True)
    mean_compound_24_hours = mean(list_compound)

    list_subjecivity = records.values_list('overall_subjectivity', flat=True)
    mean_subjectivity_24_hours = mean(list_subjecivity)

    list_polarity = records.values_list('overall_polarity', flat=True)
    mean_polarity_24_hours = mean(list_polarity)

    return JsonResponse({
        'list_ids' : list(list_ids),
        'fetched_date': fetched_date,
        'word_cloud_data': wordcloud,
        'negative_count': negative_count_24_hours,
        'positive_count': positive_count_24_hours,
        'neutral_count': negative_count_24_hours,
        'mean_negative': mean_negative_24_hours,
        'mean_positive':  mean_positive_24_hours,
        'mean_neutral':  mean_neutral_24_hours,
        'mean_polarity': mean_polarity_24_hours,
        'mean_subjectivity':  mean_subjectivity_24_hours,
        'mean_compound':  mean_compound_24_hours,
        'values_negatives':  list(list_negative),
        'values_positives':  list(list_positive),

        'values_neutral':  list(list_neutral),

        'values_compound':  list(list_compound),


        'values_polarity':  list(list_polarity),
        'values_subjectivity':  list(list_subjecivity),
        'dates' :  list(list_date)

    })





#HELPER METHOD
def mean(list_sentiment):
    return round(statistics.mean(list_sentiment) , 2)


# private method
def stemmed_text_compress(list):
    mytext = " "
    for obj in list:
        mytext += obj + " "
    return mytext

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

def generateSearchQuery(ticker):
    lower  = ticker
    uppper  = ticker.upper()
    hashtag_lower = "#" + lower
    hashtag_upper = "#" + uppper
    filter  = " -filter:retweets"
    query = lower  + " OR "  + uppper +  " OR " + hashtag_lower +  " OR " + hashtag_upper + filter
    return query