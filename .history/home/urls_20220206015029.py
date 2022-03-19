import imp
from django.contrib import admin
from django.urls import path, include
from home import views
from home.api import fetch_symbol
from singleticker.views import singleStockView

app_name =  'home'
urlpatterns = [
    path('', views.index, name="home"),
    path ('background/',views.test, name =  "background" ),
    path ('api/get_symbol/',fetch_symbol, name =  "fetch_symbols" ),
    path ('stock',singleStockView, name =  "single" ),



]
