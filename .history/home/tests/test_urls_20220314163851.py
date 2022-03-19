import imp
from django.test import SimpleTestCase

from django.urls import reverse, resolve
from home.views import home_page

class TestUrls(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url  =  reverse('home:home')
        self.assertEquals(resolve(url).func, home_page)