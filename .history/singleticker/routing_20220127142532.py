import imp
from django.urls import re_path
from django.urls import path

from singleticker import consumers

websocket_urlpatterns_stock = [
    re_path(r'ws/singlestock//(?P<stock_name>\w+)/$', consumers.SingleStockConsumer.as_asgi()),
]