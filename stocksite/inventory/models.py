from django.conf import settings
from django.db import models


class StockItem(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=30, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)


class StockMovement(models.Model):
    class Direction(models.TextChoices):
        IN = "IN", "Stock in"
        OUT = "OUT", "Stock out"

    item = models.ForeignKey(
        StockItem,
        on_delete=models.SET_NULL,
        null=True,
        related_name="movements",
    )
    item_sku = models.CharField(max_length=30)
    direction = models.CharField(max_length=3, choices=Direction.choices)
    quantity = models.PositiveIntegerField()
    quantity_before = models.PositiveIntegerField()
    quantity_after = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="stock_movements",
    )
    created_at = models.DateTimeField(auto_now_add=True)