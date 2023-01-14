from django.db import models
from django.utils.timezone import now

# Create your models here.
class products(models.Model):
    keyword = models.TextField(default='Keyword')
    title = models.TextField(default='Title')
    price_min = models.TextField(default='PriceMin')
    price_max = models.TextField(default='PriceMax')
    sold = models.TextField(default='HistoricalSold')
    store = models.TextField(default='StoreType')
    time = models.DateTimeField(default=now)
    link = models.TextField(default='Link')