
from django.test import Client, SimpleTestCase, TransactionTestCase

from django.urls import reverse





class TestApi(TransactionTestCase):
    def test_mining_tweets(self):
        userFrom = Client()
        response = userFrom.get(reverse('home:start_mining_tweets', kwargs={'ticker_id':'TSLA'})) 
        self.assertEqual(response.status_code, 200)