
from __future__ import  absolute_import, unicode_literals
from datetime import timezone
import os
from celery.schedules import crontab
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiapp.settings')

app = Celery('sentiapp')
app.conf.enable_utc =  False
app.conf.update (timezone= 'Europe/London')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


#Celery beet settings
app.conf.beat_schedule = {
    'every-60-seconds':{
        'task': 'miner.tasks.test_func2',
        'schedule' : 600,
    },
    'every-hour-create-record':{
        'task': 'miner.tasks.createHourlyRecord',
        'schedule' : crontab(minute='0', hour='*/1'),
        'args': ('TSL',),
    },
    'every-10-second-jokes':{
        'task': 'miner.tasks.get_stock_info',
        'schedule' : 10,
    }
    
}



# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')