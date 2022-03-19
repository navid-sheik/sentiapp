"""
ASGI config for sentiapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import urllib3
import miner
from home.routing import websocket_urlpatterns_home
from singleticker.consumers import SingleStockConsumer
from django.conf.urls import url
from singleticker.routing  import websocket_urlpatterns_stock
from home.consumers import HomePageConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':  AuthMiddlewareStack(
        URLRouter([
            # websocket_urlpatterns,
            url(r'ws/singlestock/(?P<stock_name>\w+)/$', SingleStockConsumer.as_asgi()),
            url(r'ws/home/$', HomePageConsumer.as_asgi()),
           
        ]),
    ),
})