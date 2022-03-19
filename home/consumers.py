from ast import arg
from email import message
import imp
from inspect import ArgInfo
import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule


from datetime import datetime
import json


class HomePageConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeatMostActivateStocks(self):
        name = "every-30-seconds" + "-" + "most-active"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)

            task.enabled = True

            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=30, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule, name=name, task="home.tasks.get_most_active")

    @sync_to_async
    def addToCeleryBeatMostVolumeStocks(self):
        name = "every-59-seconds" + "-" + "most-volume"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)

            task.enabled = True

            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=60, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule, name=name, task="home.tasks.get_most_volume")

    @sync_to_async
    def addToCeleryBeatMostGainersStocks(self):
        name = "every-25-seconds" + "-" + "most-gainers"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)

            task.enabled = True

            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=25, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule, name=name, task="home.tasks.get_most_gainers")

    @sync_to_async
    def addToCeleryBeatMostLosersStocks(self):
        name = "every-35-seconds" + "-" + "most-losers"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()

            task.enabled = True
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=35, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule, name=name, task="home.tasks.get_most_losers")

    @sync_to_async
    def addToCeleryBeatMostNasdaqStocks(self):
        name = "every-30-seconds" + "-" + "nasdaq"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            task.enabled = True
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=30, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(
                interval=schedule, name=name, task="home.tasks.get_most_nasdaq")

    async def connect(self):
        self.group_name = 'stock_%s' % "home"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.addToCeleryBeatMostActivateStocks()
        await self.addToCeleryBeatMostGainersStocks()
        await self.addToCeleryBeatMostLosersStocks()
        await self.addToCeleryBeatMostNasdaqStocks()
        await self.addToCeleryBeatMostVolumeStocks()
        await self.accept()

    @sync_to_async
    def stop_celeryBeatMostActive(self):
        name = "every-30-seconds" + "-" + "most-active"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatMostVolume(self):
        name = "every-59-seconds" + "-" + "most-volume"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatMostGainers(self):
        name = "every-25-seconds" + "-" + "most-gainers"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatMostLosers(self):
        name = "every-35-seconds" + "-" + "most-losers"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatNasdaq(self):
        name = "every-30-seconds" + "-" + "nasdaq"
        task = PeriodicTask.objects.filter(name=name)
        if len(task) > 0:
            task = task.first()
            task.enabled = False
            task.save()

    async def disconnect(self, close_code):
        await self.stop_celeryBeatMostActive()
        await self.stop_celeryBeatMostGainers()
        await self.stop_celeryBeatMostLosers()
        await self.stop_celeryBeatNasdaq()
        await self.stop_celeryBeatMostVolume()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):

        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        event = {'type': 'send_update', 'message':  message}
        print(message)

        await self.channel_layer.group_send(self.group_name, event)

   # Receive message from room group

    async def stock_update_most_active(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'most_active': message}))

      # Receive message from room group

    async def stock_update_most_volume(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'most_volume': message}))

    # Receive message from room group
    async def stock_update_most_gainers(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'most_gainers': message}))

    # Receive message from room group
    async def stock_update_most_losers(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'most_losers': message}))

     # Receive message from room group
    async def stock_update_nasdaq_price(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'nasdaq': message}))
