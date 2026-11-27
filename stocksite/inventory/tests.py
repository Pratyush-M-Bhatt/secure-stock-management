from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .models import StockItem


class StockDeleteCsrfTests(TestCase):
    def test_delete_without_csrf_token_is_rejected(self):
        manager = get_user_model().objects.create_user(username="csrf_test_manager")
        manager.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="inventory",
                codename="delete_stockitem",
            )
        )
        item = StockItem.objects.create(
            name="CSRF test item",
            sku="CSRF-TEST-001",
            quantity=1,
            reorder_level=0,
        )

        client = Client(enforce_csrf_checks=True)
        client.force_login(manager)
        url = reverse("stock_delete", kwargs={"pk": item.pk})

        self.assertEqual(client.get(url).status_code, 200)
        self.assertEqual(client.post(url, data={}).status_code, 403)
        self.assertTrue(StockItem.objects.filter(pk=item.pk).exists())