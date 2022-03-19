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

class SingleStockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeatStockInfo(self, ticker):
        name =   "every-30-seconds" +  "-" + ticker
        task  =  PeriodicTask.objects.filter(name =name)
        if len(task)>0:
            task =  task.first()
            # args =  json.loads(task.args)
            # args =  args[0]
            # if ticker not in args:
            #     args.append(ticker)
            task.args =  json.dumps([ticker])
            task.save()
        else:
            schedule, created  =  IntervalSchedule.objects.get_or_create(every = 30, period =  IntervalSchedule.SECONDS)
            task  = PeriodicTask.objects.create(interval  =  schedule, name = name, task = "singleticker.tasks.update_price", args =  json.dumps(ticker))



    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['stock_name']
        self.group_name = 'stock_%s' % self.room_name

        await self.channel_layer.group_add(self.group_name,self.channel_name)


        await   self.addToCeleryBeatStockInfo(self.room_name)
      

        await self.accept()





    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        print(text_data)
        text_data_json =  json.loads(text_data)
        message =  text_data_json['message']
        event  =    {'type' : 'stock_update', 'message' :  message}
        print(message)

        await self.channel_layer.group_send(self.group_name, event)


   # Receive message from room group
    async def stock_update(self, event):
        message =  event['message']
       
        await self.send(text_data=json.dumps({'message' : message }))
   