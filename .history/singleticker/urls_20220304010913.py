import imp
from django.contrib import admin
from django.urls import path, include
from singleticker import views
from singleticker.api import fetchStockData, fetchStockDataHistory, getHotTweet, getSentiment24Hours, getSentimentTimeRange, getSearchTwitter, getPopularTweets, getRecentTweets, get_tweets_based_sentiment, get_single_tweet_sentiment, fetchCompanyInfo
app_name = 'singleticker'

urlpatterns = [
    path('stock/<str:ticker_id>', views.singleStockView, name="single-stock"),
    path('api/get_quote/<str:ticker_id>',
         fetchStockData, name="get_current_quote"),
    path('api/get_quote/<str:ticker_id>',
         fetchCompanyInfo, name="get_company_into"),
    path('api/get_quote/<str:ticker_id>/<str:timestamp>',
         fetchStockDataHistory, name="get_time_history"),
    path('api/get_hot_tweet', getHotTweet, name="get_hot_tweet"),
    path('api/get_sentiment_last_24_hours/<str:ticker_id>',
         getSentiment24Hours, name="get_24_hours_sentiment"),
    path('api/get_time_range_sentiment/<str:ticker_id>/<int:time_range>',
         getSentimentTimeRange, name="get_time_range_sentiment"),
    path('api/get_search_tweets/<str:keyword_search>',
         getSearchTwitter, name="get_search_tweets"),
    path('api/get_popular_tweets/<str:ticker_id>',
         getPopularTweets, name="get_popular_tweets"),
    path('api/get_recent_tweets/<str:ticker_id>',
         getRecentTweets, name="get_recent_tweets"),
    path('api/get_sentimental_tweets/<str:ticker_id>',
         get_tweets_based_sentiment, name="get_sentimental_tweets"),
    path('api/get_single_tweet_sentiment/<str:sentiment_type>/<int:record_id>',
         get_single_tweet_sentiment, name="get_single_tweet_sentiment"),





]
