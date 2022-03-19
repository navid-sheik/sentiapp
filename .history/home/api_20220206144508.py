from django.http import JsonResponse

import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
def fetch_symbol(request):
    # stock_ticker = ticker_id.lower()
    # url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token=pk_8295cd8fa9064272b2335b548a28d293'

    url = 'https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey=c08b159c95da11912bebae65b95c0917'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_symbol': response})


def get_most_active(request):
    # stock_ticker = ticker_id.lower()
    # url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token=pk_8295cd8fa9064272b2335b548a28d293'

    url = 'https://cloud.iexapis.com/stable/stock/market/list/mostactive?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_symbol': response})

def get_most_gainers(request):
    # stock_ticker = ticker_id.lower()
    # url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token=pk_8295cd8fa9064272b2335b548a28d293'

    url = 'https://cloud.iexapis.com/stable/stock/market/list/gainers?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_symbol': response})

def get_most_losers(request):
    # stock_ticker = ticker_id.lower()
    # url = f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token=pk_8295cd8fa9064272b2335b548a28d293'

    url = 'https://cloud.iexapis.com/stable/stock/market/list/losers?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_symbol': response})



#change timing
def startMining(request, ticker_id):
    name  = "mining-tweets-for" + ticker_id
    schedule, createdMiner  =  IntervalSchedule.objects.get_or_create(every = 120, period =  IntervalSchedule.SECONDS)
    task  = PeriodicTask.objects.create(interval  =  schedule, name = name, task = "home.tasks.mineTweets", args =  json.dumps([ticker_id.lower()]))




    nameHourly  = "create-hourly-record-for" + ticker_id
    scheduleHourly, createdHourly  =  IntervalSchedule.objects.get_or_create(every = 250, period =  IntervalSchedule.SECONDS)
    taskHourly  = PeriodicTask.objects.create(interval  =  scheduleHourly, name = nameHourly, task = "home.tasks.createHourlyRecord", args =  json.dumps([ticker_id.lower()]))


    return JsonResponse({
        "is_miner_created" : createdMiner,
        "is_hour_created"  :  createdHourly

    })

