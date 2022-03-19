import imp
from django.test import Client, SimpleTestCase

from django.urls import reverse, resolve
from home.views import home_page




class TestViews(SimpleTestCase):
    def test_mining_tweets(self):
        userFrom = Client()
        response = userFrom.get(reverse('home:start_mining_tweets')) 
        print(response)