
import http
import requests
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from django_celery_beat.models import  HOURS, MINUTES, PeriodicTask, CrontabSchedule, IntervalSchedule

def singleStockView(request, ticker_id):
    print(ticker_id)
    context  = {}
    return render(request, 'singleticker/pages/singlestock.html', context)
    

