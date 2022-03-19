
import datetime
import statistics
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests
from celery import shared_task
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from home.models import HourlyRecord, StockSummary
import singleticker
import asyncio

channel_layer  =  get_channel_layer()
import singleticker.routing
@shared_task(bind= True)
def update_price(self, stock):
    
    url  =  f'https://cloud.iexapis.com/stable/stock/{stock}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url  =  'https://cloud.iexapis.com/stable/stock/tsla/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'
    response =  requests.get(url).json()
    joke  =  response
    print(joke)

    # print(singleticker.routing.websocket_urlpatterns)

    #send data to group
    name_room  = 'stock_%s' % stock
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send(name_room, {'type': 'stock_update', 'message' :  response}))



@shared_task(bind= True)
def update_24_hours_graph(self, ticker_id):
    
    stock_ticker = ticker_id.lower()
    # url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    url = f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/dynamic?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    print(response)
        #send data to group
    name_room  = 'stock_%s' % stock_ticker
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send(name_room, {'type': 'graph_update', 'graph' :  response}))


@shared_task(bind= True)
def update_sentiment_24Hours(self, ticker_id):

    stock_ticker = ticker_id.lower()
    stock = get_object_or_404(StockSummary, ticker=stock_ticker)
    date_from = datetime.datetime.now() - datetime.timedelta(days=2)
    records = HourlyRecord.objects.filter(
        stock=stock, tweet_date__gte=date_from)
    print("We have found this record  ",  records.count)

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

    response  =  JsonResponse({
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

    name_room  = 'stock_%s' % stock_ticker
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send(name_room, {'type': 'sentiment_update', 'sentiment' :  response}))





def mean(list_sentiment):
    return round(statistics.mean(list_sentiment) , 2)


# private method
def stemmed_text_compress(list):
    mytext = " "
    for obj in list:
        mytext += obj + " "
    return mytext
