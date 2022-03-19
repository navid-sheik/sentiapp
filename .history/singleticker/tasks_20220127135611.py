
import requests
from celery import shared_task
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import singleticker


# channel_layer  =  get_channel_layer()
import singleticker.routing
@shared_task(bind= True)
def get_stock_info ():
    return
    # url  =  'https://cloud.iexapis.com/stable/stock/tsla/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url  =  'https://cloud.iexapis.com/stable/stock/tsla/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'
    # response =  requests.get(url).json()
    # joke  =  response
    # print(joke)

    # print(singleticker.routing.websocket_urlpatterns)
    # async_to_sync(channel_layer.group_send)('stock', {'type': 'send_joke', 'message' :  joke}) 

