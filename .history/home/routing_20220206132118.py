import imp
from django.urls import re_path
from django.urls import path

from home import consumers

websocket_urlpatterns_home = [
    re_path(r'ws/home/$', consumers.HomePageConsumer.as_asgi()),
]