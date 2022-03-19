from sys import prefix
from django.http import JsonResponse
from matplotlib import ticker
import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from home.tasks import createHourlyRecord, mineTweets


def fetch_symbol(request):
    url = 'https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey=c08b159c95da11912bebae65b95c0917'
    response = requests.get(url).json()
    print(response)
    return JsonResponse({'stock_symbol': response})


def get_most_active(request):
    url = 'https://cloud.iexapis.com/stable/stock/market/list/mostactive?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_symbol': response})


def get_most_gainers(request):
    url = 'https://cloud.iexapis.com/stable/stock/market/list/gainers?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_symbol': response})


def get_most_losers(request):
    url = 'https://cloud.iexapis.com/stable/stock/market/list/losers?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_symbol': response})


def get_iex_voume(request):
    url = 'https://cloud.iexapis.com/stable/stock/market/list/iexvolume?token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_symbol': response})


def getBatchStockPrices(request, stocks):
    url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={stocks}&types=quote&token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_prices': response})


def getBatchStockNews(request, stocks):
    url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={stocks}&types=news&last=1&token=pk_8295cd8fa9064272b2335b548a28d293'
    response = requests.get(url).json()
    return JsonResponse({'stock_prices': response})

# change timing


def startMining(request, ticker_id):
    mineTweets.delay(ticker_id.lower())
    createHourlyRecord.apply_async(args=(ticker_id.lower(),), countdown=5)

    # Create periodic task for mining tweets for stocks
    name = "mining-tweets-for-" + ticker_id
    schedule, createdMiner = IntervalSchedule.objects.get_or_create(
        every=120, period=IntervalSchedule.SECONDS)
    task = PeriodicTask.objects.create(
        interval=schedule, name=name, task="home.tasks.mineTweets", args=json.dumps([ticker_id.lower()]))

    # Create periodic task for creating hourly record for stocks
    nameHourly = "create-hourly-record-for-" + ticker_id
    scheduleHourly, createdHourly = IntervalSchedule.objects.get_or_create(
        every=250, period=IntervalSchedule.SECONDS)
    taskHourly = PeriodicTask.objects.create(
        interval=scheduleHourly, name=nameHourly, task="home.tasks.createHourlyRecord", args=json.dumps([ticker_id.lower()]))

    return JsonResponse({
        "ticker_id": ticker_id,
        "is_miner_created": createdMiner,
        "is_hour_created":  createdHourly
    })


def getAllStockBeingMined(request):
    prefix = "mining-tweets-for-"
    tasks = PeriodicTask.objects.filter(name__startswith=prefix)
    nameTasks = tasks.values_list('name', flat=True)
    # split  method to get just the names
    nameAarrays = getNameOfTasks(nameTasks)
    return JsonResponse({
        "tasks": nameAarrays

    })

# Helper methods


def getNameOfTasks(queryset):
    array = []
    for name in queryset:
        splitted_name = name.split('-')
        array.append(splitted_name[-1])
    return array


def read_json_objects(data):
    decoder = json.JSONDecoder()
    offset = 0

    while offset < len(data):
        item = decoder.raw_decode(data[offset:])

        yield item[0]
        offset += item[1]
