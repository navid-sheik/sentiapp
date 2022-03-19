from django.urls import re_path

from miner import consumers
from  django.conf.urls import url
websocket_urlpatterns = [
    url(r'ws/stock/(?P<room_name>\w+)/$', consumers.StockConsumer.as_asgi()),
]