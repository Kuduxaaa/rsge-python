# Invoice Client API Reference

`rsge.InvoiceClient` provides access to the RS.ge eAPI Invoice/Declaration REST service (`https://eapi.rs.ge`), using OAuth2-style bearer token authentication.

## Constructor

```python
InvoiceClient(
    base_url:   str  = 'https://eapi.rs.ge',
    timeout:    int  = 30,
    verify_ssl: bool = True,
)
```

| Parameter | Description |
|-----------|-------------|
| `base_url` | API base URL (override for testing) |
| `timeout` | HTTP request timeout in seconds |
| `verify_ssl` | Whether to verify SSL certificates |

Supports context manager protocol:

```python
with InvoiceClient() as client:
    ...
```

---

## Authentication

The eAPI supports two authentication flows:

### One-Factor Authentication

```python
from rsge import InvoiceClient

with InvoiceClient() as client:
    auth = client.authenticate('username', 'password')
    print(f'Authenticated: {auth.access_token[:20]}...')
```

### Two-Factor Authentication (PIN)

If the account has 2FA enabled, the first `authenticate()` call returns a response with a `pin_token` but no `access_token`. The user receives a PIN code via SMS, which must be submitted with `authenticate_pin()`:

```python
from rsge import InvoiceClient

with InvoiceClient() as client:
    auth = client.authenticate('username', 'password', device_code='my-app-001')

    if auth.needs_pin:
        pin = input('Enter PIN: ')
        auth = client.authenticate_pin(
            pin_token   = auth.pin_token,
            pin         = pin,
            device_code = 'my-app-001',
        )

    invoices = client.list_invoices(TYPE=1)
```

---

## Methods

### Authentication

#### `authenticate(username, password, device_code='') -> InvoiceAuthResponse`

Authenticate with the eAPI (one-factor or first step of two-factor).

```python
def authenticate(
    self,
    username:    str,
    password:    str,
    device_code: str = '',
) -> InvoiceAuthResponse
```

| Parameter | Description |
|-----------|-------------|
| `username` | Portal username |
| `password` | Portal password |
| `device_code` | Optional device identifier GUID (for 2FA device saving) |

**Returns:** `InvoiceAuthResponse` — check `.needs_pin` for two-factor flow.

**Raises:** `RSGeAuthenticationError` if credentials are invalid.

On success, the client automatically stores the access token and sets the `Authorization` header for subsequent requests.

#### `authenticate_pin(pin_token, pin, device_code='', *, address='', browser='', oper_system='') -> InvoiceAuthResponse`

Complete two-factor authentication with a PIN code.

```python
def authenticate_pin(
    self,
    pin_token:   str,
    pin:         str,
    device_code: str = '',
    *,
    address:     str = '',
    browser:     str = '',
    oper_system: str = '',
) -> InvoiceAuthResponse
```

| Parameter | Description |
|-----------|-------------|
| `pin_token` | Token from the first authentication step |
| `pin` | The PIN code sent to the user |
| `device_code` | Device identifier GUID |
| `address` | Client IP/address (for device saving) |
| `browser` | Browser identifier |
| `oper_system` | OS identifier |

#### `sign_out() -> bool`

Sign out and invalidate the current access token. Returns `True` on success.

```python
client.sign_out()
```

#### `is_authenticated -> bool`

Property that checks whether an access token is currently set.

```python
if client.is_authenticated:
    invoices = client.list_invoices(TYPE=1)
```

---

### Common / Reference

#### `get_vat_payer_status(tin, vat_date='') -> bool`

Check if an organization is a VAT payer.

| Parameter | Description |
|-----------|-------------|
| `tin` | Tax identification number (9 or 11 digits) |
| `vat_date` | Optional date for historical check |

**Returns:** `True` if the organization is a VAT payer.

#### `get_org_info(tin) -> OrgInfo`

Get organization info by TIN.

```python
org = client.get_org_info('206322102')
print(f'{org.name} — VAT payer: {org.is_vat_payer}')
```

| Parameter | Description |
|-----------|-------------|
| `tin` | Tax identification number |

**Returns:** `OrgInfo` object with `tin`, `name`, `address`, `is_vat_payer`, `is_diplomat`.

#### `get_units() -> list[Unit]`

Get available measurement units.

```python
for unit in client.get_units():
    print(f'{unit.value}: {unit.label}')
```

**Returns:** List of `Unit` objects.

#### `get_transaction_result(transaction_id) -> TransactionResult`

Get the result of an async save transaction.

| Parameter | Description |
|-----------|-------------|
| `transaction_id` | The transaction UUID (returned by `save_invoice()`) |

**Returns:** `TransactionResult` with `invoice_id`.

---

### Invoice CRUD

#### `get_actions() -> list[InvoiceAction]`

Get available invoice statuses/actions.

```python
for action in client.get_actions():
    print(f'{action.id}: {action.name}')
```

**Returns:** List of `InvoiceAction` objects.

#### `get_invoice(invoice_id=0, invoice_number=0, parent_invoice_id=0) -> Invoice`

Get a specific invoice by ID or number.

```python
inv = client.get_invoice(invoice_id=7624)
print(f'{inv.inv_number}: {inv.tin_seller} -> {inv.tin_buyer}')
for item in inv.invoice_goods:
    print(f'  {item.goods_name}: {item.quantity} x {item.unit_price}')
```

| Parameter | Description |
|-----------|-------------|
| `invoice_id` | Invoice ID |
| `invoice_number` | Invoice number |
| `parent_invoice_id` | Parent invoice ID (for distribution sub-invoices) |

**Returns:** `Invoice` object with all nested goods, returns, advances, etc.

#### `save_invoice(invoice, transaction_id='') -> str`

Save (create or update) an invoice. For new invoices, set `id=0`.

```python
from rsge import Invoice, InvoiceCategory, InvoiceType

inv = Invoice(
    inv_category   = InvoiceCategory.GOODS_SERVICE,
    inv_type       = InvoiceType.WITH_TRANSPORT,
    operation_date = '10-04-2025 10:00:00',
    tin_seller     = '206322102',
    tin_buyer      = '12345678910',
)

inv.add_goods('Office Supplies', quantity=10, unit_price=25.50)

txn_id = client.save_invoice(inv)
result = client.get_transaction_result(txn_id)
print(f'Saved invoice ID: {result.invoice_id}')
```

| Parameter | Description |
|-----------|-------------|
| `invoice` | `Invoice` object to save |
| `transaction_id` | Optional transaction UUID (auto-generated if empty) |

**Returns:** The transaction ID (use with `get_transaction_result()` to get the invoice ID).

#### `activate_invoice(invoice, transaction_id='') -> str`

Activate an invoice (send for registration).

| Parameter | Description |
|-----------|-------------|
| `invoice` | `Invoice` object (can be minimal with just `id`) |
| `transaction_id` | Optional transaction UUID |

**Returns:** The transaction ID.

#### `activate_invoices(invoice_ids) -> bool`

Activate multiple invoices at once.

```python
client.activate_invoices([7624, 7625, 7626])
```

| Parameter | Description |
|-----------|-------------|
| `invoice_ids` | List of invoice IDs to activate |

#### `delete_invoice(invoice_id) -> bool`

Delete a saved (draft) invoice.

#### `cancel_invoice(invoice_id) -> bool`

Cancel an active/confirmed invoice (request cancellation).

#### `refuse_invoice(invoice_id) -> bool`

Refuse a received invoice (as buyer).

#### `refuse_invoices(invoice_ids) -> bool`

Refuse multiple invoices at once (as buyer).

#### `confirm_invoice(invoice_id) -> bool`

Confirm a received invoice (as buyer).

#### `confirm_invoices(invoice_ids) -> bool`

Confirm multiple invoices at once (as buyer).

#### `list_invoices(**filters) -> list[Invoice]`

List invoices with optional filters.

```python
# List seller's own documents
invoices = client.list_invoices(TYPE=1, MAXIMUM_ROWS=50)

# List buyer's received documents
invoices = client.list_invoices(TYPE=2, TIN_BUYER='12345678910')
```

Supported filter keys (all optional):

| Filter | Description |
|--------|-------------|
| `TYPE` | List type (see `InvoiceListType` enum) |
| `ID` | Invoice ID |
| `INV_NUMBER` | Invoice number |
| `INV_CATEGORY` | Category filter |
| `INV_TYPE` | Type filter |
| `ACTION` | Status/action filter |
| `TIN_BUYER` | Buyer TIN filter |
| `OPERATION_DATE` | Operation date filter |
| `MAXIMUM_ROWS` | Max rows to return |

**Returns:** List of `Invoice` objects.

#### `list_goods(invoice_ids) -> list[Invoice]`

List goods for one or more invoices.

```python
invoices = client.list_goods([7624, 7625])
for inv in invoices:
    for item in inv.invoice_goods:
        print(f'{item.goods_name}: {item.amount}')
```

#### `get_invoice_status(invoice_id) -> dict`

Get the current status of an invoice.

**Returns:** Dict with `INVOICE_ID`, `INVOICE_NUMBER`, `SELLER_ACTION`, `BUYER_ACTION`.

---

### Barcode Catalog

#### `list_bar_codes(**filters) -> list[BarCode]`

List barcode catalog entries.

```python
barcodes = client.list_bar_codes(goods_name='xaxvi')
for bc in barcodes:
    print(f'{bc.barcode}: {bc.goods_name} @ {bc.unit_price}')
```

| Parameter | Description |
|-----------|-------------|
| `barcode` | Filter by barcode value |
| `goods_name` | Filter by product name |
| `unit_txt` | Filter by unit text |
| `vat_type_txt` | Filter by VAT type text |
| `unit_price` | Filter by unit price |
| `maximum_rows` | Max rows (default 10, 0=all) |

#### `get_bar_code(barcode) -> BarCode`

Get info for a specific barcode.

#### `clear_bar_codes() -> bool`

Clear the internal barcode catalog cache.

---

### Excise

#### `list_excise(product_name='', effect_date='', end_date='', maximum_rows=10) -> list[dict]`

List excise product information.

| Parameter | Description |
|-----------|-------------|
| `product_name` | Filter by product name |
| `effect_date` | Effect date range (`DD-MM-YYYY:DD-MM-YYYY`) |
| `end_date` | End date range |
| `maximum_rows` | Max rows (default 10, 0=all) |

---

### Declaration

#### `get_seq_num(year, month=None) -> str`

Get the declaration sequence number for a period.

```python
seq = client.get_seq_num(2025)       # Yearly
seq = client.get_seq_num(2025, 4)    # Monthly (April)
```

#### `create_decl(invoice_ids, year, month=None) -> bool`

Attach invoices to a declaration for a period.

```python
client.create_decl([7624, 7625], year=2025, month=4)
```

---

## Session Management

### `close() -> None`

Close the underlying HTTP session. Called automatically when using `with` statement.

---

## Error Handling

```python
from rsge import InvoiceClient, RSGeAuthenticationError, RSGeAPIError, RSGeConnectionError

with InvoiceClient() as client:
    try:
        client.authenticate('user', 'pass')
        txn = client.save_invoice(invoice)
        result = client.get_transaction_result(txn)
    except RSGeAuthenticationError:
        print('Invalid credentials or expired token')
    except RSGeConnectionError:
        print('Cannot reach eapi.rs.ge')
    except RSGeAPIError as exc:
        print(f'API error {exc.code}: {exc.message}')
```
