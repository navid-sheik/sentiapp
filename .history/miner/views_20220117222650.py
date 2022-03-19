
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from miner.tasks import test_func2
from django_celery_beat.models import  HOURS, MINUTES, PeriodicTask, CrontabSchedule, IntervalSchedule

def test(request):
    context   = {'room-name': 'track'}
    return render(request, 'miner/pages/miner.html', context)
    