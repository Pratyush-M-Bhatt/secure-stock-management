from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import StockItemForm, StockMovementForm
from .models import StockItem, StockMovement


@login_required
@permission_required("inventory.view_stockitem", raise_exception=True)
def stock_list(request):
    all_items = StockItem.objects.all()
    items = all_items

    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    if status not in {"all", "low", "out"}:
        status = "all"

    if search:
        items = items.filter(
            Q(name__icontains=search) | Q(sku__icontains=search)
        )

    if status == "low":
        items = items.filter(quantity__lte=F("reorder_level"))
    elif status == "out":
        items = items.filter(quantity=0)

    context = {
        "items": items.order_by("name", "pk"),
        "search": search,
        "status": status,
        "stock_item_count": all_items.count(),
        "total_units": all_items.aggregate(total=Sum("quantity", default=0))["total"],
        "low_stock_count": all_items.filter(quantity__lte=F("reorder_level")).count(),
    }
    return render(request, "inventory/stock_list.html", context)


@login_required
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


@login_required
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


@login_required
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


@login_required
@permission_required("inventory.add_stockmovement", raise_exception=True)
@require_http_methods(["GET", "POST"])
def stock_move(request, pk):
    item = get_object_or_404(StockItem, pk=pk)
    form = StockMovementForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        direction = form.cleaned_data["direction"]
        quantity = form.cleaned_data["quantity"]
        before = item.quantity

        if direction == StockMovement.Direction.IN:
            after = before + quantity
        else:
            after = before - quantity

        if after < 0:
            form.add_error("quantity", "There isn't enough stock for this withdrawal.")
        elif after > 2_147_483_647:
            form.add_error("quantity", "The resulting stock quantity is too large.")
        else:
            with transaction.atomic():
                updated = StockItem.objects.filter(
                    pk=item.pk,
                    quantity=before,
                    sku=item.sku,
                ).update(quantity=after)

                if updated:
                    StockMovement.objects.create(
                        item=item,
                        item_sku=item.sku,
                        direction=direction,
                        quantity=quantity,
                        quantity_before=before,
                        quantity_after=after,
                        reason=form.cleaned_data["reason"],
                        recorded_by=request.user,
                    )

            if updated:
                return redirect("stock_list")

            form.add_error(
                None,
                "The item changed. Review the current quantity and try again.",
            )
            item = get_object_or_404(StockItem, pk=pk)

    return render(request, "inventory/stock_move.html", {"form": form, "item": item})


@login_required
@permission_required("inventory.view_stockmovement", raise_exception=True)
def stock_history(request):
    movements = StockMovement.objects.select_related("recorded_by").order_by(
        "-created_at", "-pk"
    )
    return render(
        request,
        "inventory/stock_history.html",
        {"movements": movements},
    )