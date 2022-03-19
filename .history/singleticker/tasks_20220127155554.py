
import requests
from celery import shared_task
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import singleticker
import asyncio

channel_layer  =  get_channel_layer()
import singleticker.routing
@shared_task(bind= True)
def update_price(self, stock):
    
    url  =  f'https://cloud.iexapis.com/stable/stock/{stock}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url  =  'https://cloud.iexapis.com/stable/stock/tsla/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'
    response =  requests.get(url).json()
    joke  =  response
    print(joke)

    # print(singleticker.routing.websocket_urlpatterns)

    #send data to group
    name_room  = 'stock_%s' % stock
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send(name_room, {'type': 'stock_update', 'message' :  response}))



