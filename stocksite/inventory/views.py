from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import StockItemForm
from .models import StockItem


@login_required(login_url="/admin/login/")
@permission_required("inventory.view_stockitem", raise_exception=True)
def stock_list(request):
    items = StockItem.objects.all()
    context = {
        "items": items,
        "stock_item_count": items.count(),
        "total_units": items.aggregate(total=Sum("quantity", default=0))["total"],
        "low_stock_count": items.filter(quantity__lte=F("reorder_level")).count(),
    }
    return render(request, "inventory/stock_list.html", context)


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


@login_required(login_url="/admin/login/")
@permission_required("inventory.change_stockitem", raise_exception=True)
def stock_edit(request, pk):
    item = get_object_or_404(StockItem, pk=pk)

    if request.method == "POST":
        form = StockItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("stock_list")
    else:
        form = StockItemForm(instance=item)

    return render(request, "inventory/stock_edit.html", {"form": form, "item": item})


@login_required(login_url="/admin/login/")
@permission_required("inventory.delete_stockitem", raise_exception=True)
@require_http_methods(["GET", "POST"])
def stock_delete(request, pk):
    item = get_object_or_404(StockItem, pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("stock_list")

    return render(
        request,
        "inventory/stock_confirm_delete.html",
        {"item": item},
    )