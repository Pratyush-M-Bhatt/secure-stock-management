from django import forms

from .models import StockItem, StockMovement


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ["name", "sku", "quantity", "reorder_level"]


class StockMovementForm(forms.Form):
    direction = forms.ChoiceField(choices=StockMovement.Direction.choices)
    quantity = forms.IntegerField(min_value=1, max_value=2_147_483_647)
    reason = forms.CharField(max_length=255)