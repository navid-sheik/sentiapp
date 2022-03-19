
import http
from urllib import requests
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from django_celery_beat.models import  HOURS, MINUTES, PeriodicTask, CrontabSchedule, IntervalSchedule

def singleStockView(request, ticker_id):
    print(ticker_id)
    context  = {}
    fetchStockData(ticker_id)
    return render(request, 'singleticker/pages/singlestock.html', context)
    
def fetchStockData(ticker_id):
    stock_ticker =  ticker_id.lower()
    url  =  f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'
    response =  requests.get(url).json()

    print(response)
