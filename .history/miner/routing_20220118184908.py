from importlib.resources import path
from django.urls import re_path

from miner import consumers

websocket_urlpatterns = [
    path('ws/stock/', consumers.StockConsumer.as_asgi()),
]