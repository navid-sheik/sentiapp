import imp
from django.urls import re_path
from django.urls import path

from singleticker import consumers

websocket_urlpatterns = [
    re_path(r'ws/singlestock/$', consumers.SingleStockConsumer.as_asgi()),
]