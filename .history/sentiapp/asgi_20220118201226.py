"""
ASGI config for sentiapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
from importlib.resources import path
from django.conf.urls import url
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from miner.routing  import websocket_urlpatterns
from miner.consumers import StockConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':  AuthMiddlewareStack(
        URLRouter(
            [
                url(r'ws/stock/', StockConsumer)
            ]
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})