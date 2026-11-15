from django.db import models

# Create your models here.
class StockItem(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=30, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)