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

class SingleStockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeatStockInfo(self, ticker):
        
        name =  ticker.lower() +  "-" +  "every-minute-update-price" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)
            task.args =  json.dumps([ticker.lower()])
            task.enabled = True
            
            task.save()
        else:
            #every minutes
            schedule, created  =  IntervalSchedule.objects.get_or_create(every = 60, period =  IntervalSchedule.SECONDS)
            print(ticker)
            task  = PeriodicTask.objects.create(interval  =  schedule, name = name, task = "singleticker.tasks.update_price", args =  json.dumps([ticker]))


    @sync_to_async
    def addToCeleryBeatStockIGraphInfo(self, ticker):
        name =  ticker.lower() +  "-" +  "every-10-minutes-graph-price" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)
            task.args =  json.dumps([ticker.lower()])
            task.enabled = True
            
            task.save()
        else:
            schedule, created  =  IntervalSchedule.objects.get_or_create(every = 600, period =  IntervalSchedule.SECONDS)
            print(ticker)
            task  = PeriodicTask.objects.create(interval  =  schedule, name = name, task = "singleticker.tasks.update_24_hours_graph", args =  json.dumps([ticker]))


    @sync_to_async
    def addToCeleryBeatStockISentimentInfo(self, ticker):
        name =   ticker.lower() +  "-" +  "every-31-minutes-sentiment" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)
            task.args =  json.dumps([ticker.lower()])
            task.enabled = True
            
            task.save()
        else:
            #every 31 minutes update sentiment sentiment
            schedule, created  =  IntervalSchedule.objects.get_or_create(every = 1860, period =  IntervalSchedule.SECONDS)
            print(ticker)
            task  = PeriodicTask.objects.create(interval  =  schedule, name = name, task = "singleticker.tasks.update_sentiment_24Hours", args =  json.dumps([ticker]))


    @sync_to_async
    def addToCeleryBeatRecentTweets(self, ticker):
        name =  ticker.lower() +  "-" +  "every-12-minutes-recent=tweets" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)
            task.args =  json.dumps([ticker.lower()])
            task.enabled = True
            
            task.save()
        else:
            #every 12 minutes 
            schedule, created  =  IntervalSchedule.objects.get_or_create(every = 720, period =  IntervalSchedule.SECONDS)
            print(ticker)
            task  = PeriodicTask.objects.create(interval  =  schedule, name = name, task = "singleticker.tasks.update_recent_tweets", args =  json.dumps([ticker]))



    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['stock_name']
        self.group_name = 'stock_%s' % self.room_name

        await self.channel_layer.group_add(self.group_name,self.channel_name)


        await   self.addToCeleryBeatStockInfo(self.room_name)
        await   self.addToCeleryBeatStockIGraphInfo(self.room_name)
        await   self.addToCeleryBeatStockISentimentInfo(self.room_name)
        await   self.addToCeleryBeatRecentTweets(self.room_name)

        await self.accept()





    @sync_to_async
    def stop_celeryBeatStockInfo(self, ticker):
        name =  ticker.lower() +  "-" +  "every-minute-update-price" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatStockGraphInfo(self, ticker):
        name =  ticker.lower() +  "-" +  "every-10-minutes-graph-price" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatStockSentimentInfo(self, ticker):
        name =   ticker.lower() +  "-" +  "every-31-minutes-sentiment" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            task.enabled = False
            task.save()

    @sync_to_async
    def stop_celeryBeatTweetsRecent(self, ticker):
        name =  ticker.lower() +  "-" +  "every-12-minutes-recent=tweets" 
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            task.enabled = False
            task.save()



    async def disconnect(self, close_code):
        await self.stop_celeryBeatStockInfo(self.room_name)
        await self.stop_celeryBeatStockGraphInfo(self.room_name)
        await self.stop_celeryBeatStockSentimentInfo(self.room_name)
        await self.stop_celeryBeatTweetsRecent(self.room_name)
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        print(text_data)
        text_data_json =  json.loads(text_data)
        message =  text_data_json['message']
        event  =    {'type' : 'send_update', 'message' :  message}
        print(message)

        await self.channel_layer.group_send(self.group_name, event)


   # Receive message from room group
    async def stock_update(self, event):
        message =  event['message']
       
        await self.send(text_data=json.dumps( message ))

     # Receive message from room group
    async def graph_update(self, event):
        message =  event['graph']
       
        await self.send(text_data=json.dumps( {'graph' :message} ))

     # Receive message from room group
    async def sentiment_update(self, event):
        message =  event['sentiment']
        
        await self.send(text_data=json.dumps( {'sentiment' :message} ))

    async def tweets_recent_update(self, event):
        message =  event['tweets_recent']
        
        await self.send(text_data=json.dumps( {'tweets_recent' :message} ))
   
   





