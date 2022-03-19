
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from miner.tasks import test_func2
from django_celery_beat.models import  HOURS, MINUTES, PeriodicTask, CrontabSchedule, IntervalSchedule

def test(request):
 
    return render(request, 'singleticker/pages/miner.html', {})
    