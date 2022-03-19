from django.contrib import admin
from .models import HourlyRecord, StockSummary, TweetRecord

class HourlyRecord(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(StockSummary)
admin.site.register(TweetRecord)
admin.site.register(HourlyRecord)
# Register your models here.
