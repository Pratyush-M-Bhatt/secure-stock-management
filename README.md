# Secure Stock Management

## 15 November 2026
- Set up the Django project in VS Code on Windows.
- Created the inventory app and applied the database migration for StockItem.
- Registered StockItem in Django Admin and saved a sample Hammer record.
- Configured Stock Staff with view-only access and Stock Managers with permission to view, add, edit, and delete stock items.

## 22 November 2026

- Tested the Stock Staff account in Django Admin and confirmed it could view the Hammer record with read-only fields.
- Tested the Stock Managers account in Django Admin and confirmed it could edit and save a stock item.
- Built a stock list at `/stock/` that requires sign-in and the `inventory.view_stockitem` permission.
- Confirmed locally that the styled table displays the Hammer record with its SKU, quantity, and reorder level.

## 23 November 2026

- Added a Django form, view, and URL for creating stock items at `/stock/add/`. The view requires sign-in and the `inventory.add_stockitem` permission.
- Moved `stock_add.html` into the app's template folder beside `stock_list.html` after Django reported a missing template.
- Pending local verification: confirm that `stock_manager` can save an item and that `stock_staff` receives a 403 response.
