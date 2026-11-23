from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render

from .forms import StockItemForm
from .models import StockItem


@login_required(login_url="/admin/login/")
@permission_required("inventory.view_stockitem", raise_exception=True)
def stock_list(request):
    items = StockItem.objects.all()
    return render(request, "inventory/stock_list.html", {"items": items})


@login_required(login_url="/admin/login/")
@permission_required("inventory.add_stockitem", raise_exception=True)
def stock_add(request):
    if request.method == "POST":
        form = StockItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stock_list")
    else:
        form = StockItemForm()

    return render(request, "inventory/stock_add.html", {"form": form})