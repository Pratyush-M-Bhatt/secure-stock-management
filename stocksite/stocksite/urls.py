from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from inventory.views import stock_add, stock_delete, stock_edit, stock_list, stock_move

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="inventory/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("stock/", stock_list, name="stock_list"),
    path("stock/add/", stock_add, name="stock_add"),
    path("stock/<int:pk>/edit/", stock_edit, name="stock_edit"),
    path("stock/<int:pk>/delete/", stock_delete, name="stock_delete"),
    path("stock/<int:pk>/move/", stock_move, name="stock_move"),
]