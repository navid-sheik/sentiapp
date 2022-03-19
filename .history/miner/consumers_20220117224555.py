import json
from channels.generic.websocket import WebsocketConsumer

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class StockConsumer(WebsocketConsumer):
    async def connect(self):
        await self.chanel_layer.group_add('stock', self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.chanel_layer.group_discard('stock', self.channel_name)




    # Receive message from room group
    def send_joke(self, event):
        message = event['text']

        await self.send(message)