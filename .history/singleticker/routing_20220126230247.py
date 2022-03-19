import imp
from django.urls import re_path
from django.urls import path

from miner import consumers

websocket_urlpatterns = [
    re_path(r'ws/singlestock/$', consumers.StockConsumer.as_asgi()),
]