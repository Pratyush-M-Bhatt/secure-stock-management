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
- Added SKU search and Stock in / Stock out filters to Movement history for users with the `inventory.view_stockmovement` permission.
- Verified as Stock Manager that `HAM-001` returned two Stock out records and three Stock in records, and that Clear filters restored all six movements.

## Security validation checklist

Use disposable records in the local development environment. Record the expected result, actual result, and evidence for each check.

- [ ] Login and logout: signed-out users are redirected to login, and protected pages require login again after logout.
- [ ] Role permissions: Stock Staff can browse and filter inventory. Verify that direct requests to Manager-only pages return HTTP 403 for Stock Staff and that a Stock Manager can open Movement history.
- [ ] Form and URL validation: check blank required fields, duplicate SKUs, invalid quantities, and malformed or missing item IDs. Confirm rejected input leaves inventory unchanged.
- [ ] Stock integrity: verify that invalid withdrawals leave both the item quantity and movement history unchanged. Confirm a valid adjustment records the before and after quantities and the user.
- [ ] SQL injection prevention: review item lookups and search filters for parameterized ORM usage, check for raw SQL assembled from request input, and verify that a SKU containing an apostrophe is handled as literal search text.
- [ ] CSRF and delete confirmation: rerun the automated check for a delete POST without a CSRF token. Confirm it returns HTTP 403 and preserves the item. Verify that opening the confirmation page preserves the item.
- [ ] Final review: rerun the Django tests and Bandit, review tracked files for secrets, and record the results for the demo.
