# WayBill Client API Reference

`rsge.WayBillClient` is the primary interface for all electronic waybill operations against the RS.ge SOAP service.

## Constructor

```python
WayBillClient(
    service_user:     str,
    service_password: str,
    base_url:         str  = 'https://services.rs.ge/WayBillService/WayBillService.asmx',
    timeout:          int  = 30,
    verify_ssl:       bool = True,
)
```

| Parameter | Description |
|-----------|-------------|
| `service_user` | Service username (`su` parameter) from RS.ge declarant portal |
| `service_password` | Service password (`sp` parameter) |
| `base_url` | SOAP endpoint URL (override for testing) |
| `timeout` | HTTP request timeout in seconds |
| `verify_ssl` | Whether to verify SSL certificates |

Supports context manager protocol:

```python
with WayBillClient('user', 'pass') as client:
    ...
```

---

## Authentication & Service Users

### `check_service_user() -> tuple[int, int]`

Verify credentials and return account identifiers.

```python
un_id, s_user_id = client.check_service_user()
```

**Returns:** `(un_id, s_user_id)` tuple.

**Raises:** `RSGeAuthenticationError` if credentials are invalid.

### `get_service_users(user_name, user_password) -> list[ServiceUser]`

List all service users under a declarant account.

```python
users = client.get_service_users('portal_user', 'portal_pass')
for u in users:
    print(f'{u.id}: {u.user_name} (IP: {u.ip})')
```

### `update_service_user(user_name, user_password, ip, name) -> bool`

Update a service user's registration (IP whitelist and object name).

```python
ok = client.update_service_user(
    user_name     = 'portal_user',
    user_password = 'portal_pass',
    ip            = '203.0.113.10',
    name          = 'Warehouse #2',
)
```

---

## Creating & Saving Waybills

### `create_waybill(...) -> WayBill`

Create a new waybill object in memory (does **not** save to server).

```python
waybill = client.create_waybill(
    waybill_type         = WayBillType.TRANSPORTATION,
    buyer_tin            = '12345678901',
    buyer_name           = 'Buyer LLC',
    start_address        = 'Tbilisi',
    end_address          = 'Batumi',
    driver_tin           = '01234567890',
    driver_name          = 'Driver Name',
    car_number           = 'AB-123-CD',
    transport_cost       = 100.0,
    transport_cost_payer = TransportCostPayer.SELLER,
    comment              = 'Fragile goods',
)
```

**Full signature:**

```python
def create_waybill(
    self,
    waybill_type:         WayBillType | int     = WayBillType.TRANSPORTATION,
    buyer_tin:            str                    = '',
    buyer_name:           str                    = '',
    start_address:        str                    = '',
    end_address:          str                    = '',
    *,
    check_buyer_tin:      int                    = 1,
    driver_tin:           str                    = '',
    check_driver_tin:     int                    = 1,
    driver_name:          str                    = '',
    car_number:           str                    = '',
    transport_cost:       float                  = 0,
    transport_cost_payer: TransportCostPayer | int = TransportCostPayer.SELLER,
    transport_type_id:    int                    = 1,
    transport_type_txt:   str                    = '',
    comment:              str                    = '',
    category:             CategoryType | int     = CategoryType.REGULAR,
    is_medicine:          int                    = 0,
    parent_id:            str                    = '',
    transporter_tin:      str                    = '',
) -> WayBill
```

After creating, add goods items:

```python
waybill.add_goods(
    name     = 'Product A',
    unit_id  = 1,
    quantity = 5,
    price    = 10.0,
    bar_code = '1234567890',
)
```

### `save_waybill(waybill) -> WayBillSaveResult`

Save (create or update) a waybill on the RS.ge server.

```python
result = client.save_waybill(waybill)
if result.is_success:
    print(f'Waybill ID: {result.waybill_id}')
else:
    print(f'Error status: {result.status}')
```

Set `waybill.id = 0` for new waybills, or set to an existing ID to update.

---

## Retrieving Waybills

### `get_waybill(waybill_id) -> WayBill`

Retrieve a single waybill by ID with all fields and goods items populated.

```python
wb = client.get_waybill(12345)
print(f'Status: {wb.status}, Items: {len(wb.goods_list)}')
```

### `get_waybills(**filters) -> list[WayBillListItem]`

List seller-side waybills with optional filters.

```python
items = client.get_waybills(
    create_date_s = '2024-01-01',
    create_date_e = '2024-01-31',
    statuses      = '1',
)
```

### `get_buyer_waybills(**filters) -> list[WayBillListItem]`

List buyer-side waybills with optional filters.

```python
items = client.get_buyer_waybills(seller_tin='12345678901')
```

### `get_waybills_ex(**filters, is_confirmed) -> list[WayBillListItem]`

Extended seller-side query with confirmation status filter.

```python
items = client.get_waybills_ex(is_confirmed=1)
```

### `get_buyer_waybills_ex(**filters, is_confirmed) -> list[WayBillListItem]`

Extended buyer-side query with confirmation status filter.

### `get_waybills_v1(last_update_date_s, last_update_date_e, buyer_tin='') -> list[WayBillListItem]`

List waybills by last-update date range (max 3 days).

```python
items = client.get_waybills_v1(
    last_update_date_s = '2024-01-01',
    last_update_date_e = '2024-01-03',
)
```

**Common filter parameters** (shared by `get_waybills`, `get_buyer_waybills`, and `_ex` variants):

| Parameter | Description |
|-----------|-------------|
| `types` | Waybill type IDs (comma-separated) |
| `statuses` | Status codes (comma-separated) |
| `car_number` | Vehicle number filter |
| `begin_date_s` / `begin_date_e` | Transport start date range |
| `create_date_s` / `create_date_e` | Creation date range |
| `driver_tin` | Driver TIN filter |
| `delivery_date_s` / `delivery_date_e` | Delivery date range |
| `full_amount` | Total amount filter |
| `waybill_number` | Waybill number filter |
| `close_date_s` / `close_date_e` | Close date range |
| `s_user_ids` | Service user IDs filter |
| `comment` | Comment text filter |

---

## Waybill Lifecycle

### `activate_waybill(waybill_id) -> str`

Activate a saved waybill (start transportation). Returns the assigned waybill number.

```python
number = client.activate_waybill(result.waybill_id)
print(f'Waybill number: {number}')
```

### `activate_waybill_with_date(waybill_id, begin_date) -> str`

Activate with a specific transport start date. Accepts `datetime` or ISO string.

```python
from datetime import datetime

number = client.activate_waybill_with_date(
    waybill_id = 12345,
    begin_date = datetime(2024, 6, 15, 9, 0),
)
```

### `close_waybill(waybill_id) -> int`

Close/complete a waybill. Returns `1` on success.

```python
code = client.close_waybill(12345)
```

**Raises:** `RSGeAPIError` on failure (e.g., error code `-100` for invalid credentials).

### `close_waybill_with_date(waybill_id, delivery_date) -> int`

Close with a specific delivery date.

### `delete_waybill(waybill_id) -> int`

Delete a saved (non-activated) waybill. Returns `1` on success.

### `cancel_waybill(waybill_id) -> int`

Cancel (void) an activated waybill. Returns `1` on success.

---

## Buyer Confirmation

### `confirm_waybill(waybill_id) -> bool`

Confirm (accept) a waybill as the buyer.

```python
ok = client.confirm_waybill(12345)
```

### `reject_waybill(waybill_id) -> bool`

Reject a waybill as the buyer.

---

## Transporter Operations

These methods are for transporter companies handling forwarded waybills.

### `save_waybill_transporter(waybill_id, car_number, driver_tin, driver_name, **kwargs) -> int`

Save transporter-specific fields on a forwarded waybill.

```python
code = client.save_waybill_transporter(
    waybill_id        = 12345,
    car_number        = 'TR-999-GE',
    driver_tin        = '98765432101',
    driver_name       = 'Transport Driver',
    transport_type_id = 1,
)
```

### `activate_waybill_transporter(waybill_id, begin_date) -> tuple[int, str]`

Activate a waybill as transporter. Returns `(code, waybill_number)`.

### `close_waybill_transporter(waybill_id, delivery_date, reception_info='', receiver_info='') -> int`

Close a waybill as transporter.

---

## Invoices

### `save_invoice(waybill_id, invoice_id=0) -> tuple[int, int]`

Issue a tax invoice from a waybill. Returns `(code, invoice_id)`.

```python
code, inv_id = client.save_invoice(waybill_id=12345)
```

---

## Templates

### `save_waybill_template(name, waybill) -> int`

Save a waybill as a reusable template. Returns `1` on success.

```python
waybill = client.create_waybill(
    waybill_type  = WayBillType.TRANSPORTATION,
    start_address = 'Tbilisi',
    end_address   = 'Batumi',
)

code = client.save_waybill_template('Tbilisi to Batumi', waybill)
```

### `get_waybill_templates() -> list[dict[str, Any]]`

List all saved templates. Each dict has `'id'` and `'name'` keys.

### `get_waybill_template(template_id) -> WayBill`

Retrieve a template by ID as a `WayBill` object.

### `delete_waybill_template(template_id) -> int`

Delete a template. Returns `1` on success.

---

## Barcode Catalog

### `save_bar_code(bar_code, goods_name, unit_id, unit_txt='', akciz_id=0) -> int`

Save a barcode to the personal catalog. Returns `1` on success.

```python
client.save_bar_code(
    bar_code   = '5901234123457',
    goods_name = 'Office Paper A4',
    unit_id    = 1,
)
```

### `delete_bar_code(bar_code) -> int`

Delete a barcode from the catalog.

### `get_bar_codes(bar_code='') -> list[dict[str, Any]]`

List barcodes from the personal catalog. Each dict contains: `bar_code`, `goods_name`, `unit_id`, `unit_txt`, `a_id`.

---

## Vehicle Registration

### `save_car_number(car_number) -> int`

Register a vehicle for distribution waybills.

### `delete_car_number(car_number) -> int`

Remove a registered vehicle.

### `get_car_numbers() -> list[str]`

List all registered vehicle numbers.

---

## Reference Data

### `get_name_from_tin(tin) -> str`

Look up a taxpayer's registered name by TIN or personal number.

```python
name = client.get_name_from_tin('12345678901')
```

### `get_akciz_codes() -> list[AkcizCode]`

Retrieve excise (akciz) commodity codes.

### `get_waybill_types() -> list[WayBillTypeInfo]`

Retrieve waybill type reference list.

### `get_waybill_units() -> list[WayBillUnit]`

Retrieve measurement unit reference list.

### `get_transport_types() -> list[TransportType]`

Retrieve transportation type reference list.

### `get_wood_types() -> list[WoodType]`

Retrieve wood/timber type reference list.

### `get_error_codes() -> list[ErrorCode]`

Retrieve API error codes and their descriptions.

---

## Session Management

### `close() -> None`

Close the underlying HTTP session. Called automatically when using `with` statement.

```python
client = WayBillClient('user', 'pass')
try:
    ...
finally:
    client.close()
```
