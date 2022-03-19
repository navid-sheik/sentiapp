from importlib.resources import path
from django.urls import re_path

from miner import consumers
from  django.conf.urls import url
websocket_urlpatterns = [
    path(r'ws/stock/', consumers.StockConsumer.as_asgi()),
]