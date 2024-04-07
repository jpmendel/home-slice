from django.db import models


class StockHistory(models.Model):
    symbol = models.CharField(primary_key=True, max_length=32)
    created_at = models.DateTimeField(auto_now=True)
