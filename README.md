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
- Added a navy sidebar with an Inventory link and an Inventory Dashboard heading. Confirmed locally that the table still displays Hammer (HAM-001), quantity 20, and reorder level 5.

## 26 November 2026

- Tested the dashboard summary cards and icons in the local development environment.
- Confirmed that Stock Managers can add an item from the dashboard and that the inventory totals update after saving.
- Confirmed that the Stock Staff dashboard hides the add button and that opening `/stock/add/` directly returns HTTP 403.
- Prepared the stock edit view, route, form template, and dashboard link locally.

## 27 November 2026

- Verified that a manager can edit stock and that Staff receive HTTP 403 when opening Edit and Delete URLs directly.
- Added a Delete confirmation page and updated the Edit form layout.
- Verified locally that the dashboard loads the three SVG warehouse illustrations.
- Added a shared stock sign-in page and a logout icon to the inventory dashboard.
- Implemented Stock In and Stock Out locally with a permission-controlled adjustment form and a transaction that saves the new quantity and movement record together.
- Confirmed locally that the dashboard displays the Adjust stock action for an account with the required permission.

## 28 November 2026

- Added dashboard search by item name or SKU for Stock Staff and Stock Managers.
- Added All, Low stock, and Out of stock filters, with a Clear filters link to restore the full inventory list.
- Kept the summary cards based on the full inventory while the table is filtered.
- Verified SKU search and stock status filtering on the Stock Staff dashboard.
