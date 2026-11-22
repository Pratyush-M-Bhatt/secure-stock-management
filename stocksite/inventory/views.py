from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


from .models import StockItem
@login_required(login_url="/admin/login/")
@permission_required("inventory.view_stockitem", raise_exception=True)
def stock_list(request):
    items = StockItem.objects.all()
    return render(request, "inventory/stock_list.html", {"items": items})