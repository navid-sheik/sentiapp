import imp
from django.contrib import admin
from django.urls import path, include
from home import views
from home.api import fetch_symbol, get_most_active, get_most_gainers, get_most_losers
from singleticker.views import singleStockView

app_name =  'home'
urlpatterns = [
    path('', views.index, name="home"),
    path ('background/',views.test, name =  "background" ),

    path ('stock/<str:ticker_id>',singleStockView, name =  "single" ),
    path ('api/get_symbol/',fetch_symbol, name =  "fetch_symbols" ),
    path ('api/get_most_active/',get_most_active, name =  "get_most_active" ),
    path ('api/get_most_gainers/',get_most_gainers, name =  "get_most_gainers" ),
    path ('api/get_most_losers/',get_most_losers, name =  "get_most_losers" ),



]
