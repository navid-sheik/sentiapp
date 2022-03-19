from email import message
import json
from channels.generic.websocket import WebsocketConsumer

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class StockConsumer(WebsocketConsumer):
    async def connect(self):
        self.group_name   =  "stock"
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json =  json.loads(text_data)
        message =  text_data_json['message']
        event  =    {'type' : 'send_joke', 'message' :  message
        
        }

        await self.channel_layer.group_send(self.group_name, event)
    # Receive message from room group
    async def send_joke(self, event):
        message =  event['message']
        await self.send(text_data=json.dumps({'message' : message }))