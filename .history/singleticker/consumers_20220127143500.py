from email import message
import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class SingleStockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['stock_name']
        self.group_name = 'stock_%s' % self.room_name

        await self.channel_layer.group_add(self.group_name,self.channel_name)


        
        print("The channel name is " + self.channel_name)

        await self.accept()





    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        return
        # print(text_data)
        # text_data_json =  json.loads(text_data)
        # message =  text_data_json['message']
        # event  =    {'type' : 'send_joke', 'message' :  message
        
        # }
        # print(message)

        # await self.channel_layer.group_send(self.group_name, event)
    # Receive message from room group
    async def send_joke(self, event):
        # message =  event['message']
        # print(message)
        # await self.send(text_data=json.dumps({'message' : message }))
        return