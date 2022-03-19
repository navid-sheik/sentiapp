
from django.test import Client, SimpleTestCase, TransactionTestCase

from django.urls import reverse





class TestViews(TransactionTestCase):
    def test_mining_tweets(self):
        userFrom = Client()
        response = userFrom.get(reverse('home:start_mining_tweets', kwargs={'ticker_id':'TSLA'})) 
        print(response)