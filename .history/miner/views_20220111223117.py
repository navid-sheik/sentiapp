
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from miner.tasks import test_func2
from django_celery_beat.models import  HOURS, MINUTES, PeriodicTask, CrontabSchedule, IntervalSchedule

def test(request):

    create, schedule  = IntervalSchedule.objects.get_or_create(every=10,period=IntervalSchedule.SECONDS)
    task  =  PeriodicTask.objects.create(crontab = schedule, name = "schedule_tweet" + "1", task="miner.tasks.test_func2")
    return HttpResponse("Done")