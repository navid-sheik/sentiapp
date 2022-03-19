from pickle import TRUE
from pyexpat import model
from unicodedata import name
from django.db import models

# Create your models here.
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, DateTimeField, IntegerField


class StockSummary(models.Model):

    ticker  =  models.CharField(primary_key=True, max_length=200, unique=True )
    last_fetched  = models.DateTimeField("last_fetched", null=True)

    def __str__(self) -> str:
        return self.ticker






class TweetRecord(models.Model):
    stock = models.ForeignKey(StockSummary, on_delete=models.CASCADE, default="TSL")
    tweet_id =  models.CharField(primary_key=True, max_length=100, default="1")
    tweet_date =  models.DateTimeField("date_fetched", null=True)
    raw_text = models.CharField(max_length=10000)
    processed_text = models.CharField(max_length=10000)
    stemmed_text =  models.CharField(max_length=10000, null=True)
    polarity = models.DecimalField(max_digits=20, decimal_places=6)
    sentiment  =  models.CharField(max_length=200)
    subjectivity =  models.DecimalField(max_digits=20, decimal_places=6)
    neg =  models.DecimalField(max_digits=20, decimal_places=3)
    neu =  models.DecimalField(max_digits=20, decimal_places=3)
    pos  = models.DecimalField(max_digits=20, decimal_places=3)
    compound  = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self) -> str:
        return self.tweet_id


class HourlyRecord (models.Model):
    stock = models.ForeignKey(StockSummary, on_delete=models.CASCADE, default="TSL")
    tweet_date =  models.DateTimeField("date_fetched", null=True)
    overall_polarity =   models.DecimalField(max_digits=20, decimal_places=6)
    overall_stemmed_text =  models.CharField(max_length=10000, null=True)
    overall_sentiment  =  models.CharField(max_length=200)
    overall_subjectivity =  models.DecimalField(max_digits=20, decimal_places=6)
    overall_neg =  models.DecimalField(max_digits=20, decimal_places=3)
    overall_neu =  models.DecimalField(max_digits=20, decimal_places=3)
    overall_pos  = models.DecimalField(max_digits=20, decimal_places=3)
    overall_compound  = models.DecimalField(max_digits=20, decimal_places=4)
    negative_count  =  models.IntegerField()
    positive_count  =  models.IntegerField()
    negative_count  =  models.IntegerField()

    def __str__(self) -> str:
        return str(self.tweet_date)


class DailyRecord (models.Model):
    stock = models.ForeignKey(StockSummary, on_delete=models.CASCADE, default="TSL")
    tweet_date =  models.DateTimeField("date_fetched", null=True)
    overall_polarity =   models.DecimalField(max_digits=20, decimal_places=6)

    overall_sentiment  =  models.CharField(max_length=200)
    overall_subjectivity =  models.DecimalField(max_digits=20, decimal_places=6)
    overall_neg =  models.DecimalField(max_digits=20, decimal_places=3)
    overall_neu =  models.DecimalField(max_digits=20, decimal_places=3)
    overall_pos  = models.DecimalField(max_digits=20, decimal_places=3)
    overall_compound  = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self) -> str:
        return self.tweet_date

class MonthlyRecord (models.Model):
    stock = models.ForeignKey(StockSummary, on_delete=models.CASCADE, default="TSL")
    tweet_date =  models.DateTimeField("date_fetched", null=True)
    overall_polarity =   models.DecimalField(max_digits=20, decimal_places=6)

    overall_sentiment  =  models.CharField(max_length=200)
    overall_subjectivity =  models.DecimalField(max_digits=20, decimal_places=6)
    overall_neg =  models.DecimalField(max_digits=20, decimal_places=3)
    overall_neu =  models.DecimalField(max_digits=20, decimal_places=3)
    overall_pos  = models.DecimalField(max_digits=20, decimal_places=3)
    overall_compound  = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self) -> str:
        return self.tweet_date




