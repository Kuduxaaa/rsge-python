# Models Reference

All models are Python dataclasses that serialize to/from XML (waybill models) or JSON (customs and invoice models) for communication with the RS.ge APIs. Import them directly from `rsge`:

```python
from rsge import WayBill, GoodsItem, WayBillSaveResult, CustomsDeclaration
from rsge import Invoice, InvoiceGoods, InvoiceAuthResponse, OrgInfo
```

---

## WayBill Models

### `WayBill`

Complete electronic commodity waybill. The primary model for creating, saving, and retrieving waybills.

**Source:** `rsge/waybill/models.py`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Waybill ID (0 for new waybills) |
| `waybill_type` | `WayBillType \| int` | `WayBillType.TRANSPORTATION` | Type of waybill |
| `buyer_tin` | `str` | `''` | Buyer's personal/identification number |
| `check_buyer_tin` | `int` | `1` | 1 if Georgian citizen, 0 if foreign |
| `buyer_name` | `str` | `''` | Buyer's name |
| `start_address` | `str` | `''` | Transportation start address |
| `end_address` | `str` | `''` | Transportation end address |
| `driver_tin` | `str` | `''` | Driver's personal number |
| `check_driver_tin` | `int` | `1` | 1 if Georgian citizen, 0 if foreign |
| `driver_name` | `str` | `''` | Driver's name |
| `transport_cost` | `float` | `0` | Transportation cost |
| `reception_info` | `str` | `''` | Supplier/sender information |
| `receiver_info` | `str` | `''` | Receiver information |
| `delivery_date` | `str` | `''` | Delivery date (fill before closing) |
| `status` | `WayBillStatus \| int` | `WayBillStatus.SAVED` | Current waybill status |
| `seller_un_id` | `int` | `0` | Seller's unique number |
| `parent_id` | `str` | `''` | Parent waybill ID (for sub-waybills) |
| `full_amount` | `float` | `0` | Total waybill amount (auto-calculated) |
| `car_number` | `str` | `''` | Vehicle registration number |
| `waybill_number` | `str` | `''` | Assigned waybill number (set by server) |
| `s_user_id` | `int` | `0` | Service user ID |
| `begin_date` | `str` | `''` | Transportation start date |
| `transport_cost_payer` | `TransportCostPayer \| int` | `TransportCostPayer.SELLER` | Who pays transport cost |
| `transport_type_id` | `int` | `1` | Transport type ID |
| `transport_type_txt` | `str` | `''` | Transport type text (when type is "other") |
| `comment` | `str` | `''` | Freeform comment |
| `category` | `CategoryType \| int` | `CategoryType.REGULAR` | Waybill category (regular or wood) |
| `is_medicine` | `int` | `0` | 1 if medicine waybill |
| `wood_labels` | `str` | `''` | Timber label numbers |
| `transporter_tin` | `str` | `''` | Transporter company TIN (for forwarded waybills) |
| `goods_list` | `list[GoodsItem]` | `[]` | List of goods/product items |
| `wood_docs_list` | `list[WoodDocument]` | `[]` | List of wood-origin documents |
| `sub_waybills` | `list[SubWayBill]` | `[]` | List of sub-waybill references |
| `create_date` | `str` | `''` | Creation date (read-only, set by server) |
| `activate_date` | `str` | `''` | Activation date (read-only) |
| `close_date` | `str` | `''` | Closing date (read-only) |
| `customs_status` | `str` | `''` | Customs confirmation status |
| `customs_name` | `str` | `''` | Customs checkpoint name |

**Methods:**

- `add_goods(name, unit_id, quantity, price, bar_code, **kwargs) -> GoodsItem` — add a goods item and auto-recalculate `full_amount`
- `add_wood_document(doc_number, doc_date, doc_description) -> WoodDocument` — add a wood-origin document
- `to_xml() -> ET.Element` — serialize to XML for the SOAP API
- `WayBill.from_xml(elem) -> WayBill` — parse from XML response

---

### `GoodsItem`

A single goods/product line item within a waybill.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Record ID (0 for new items) |
| `name` | `str` | `''` | Product name |
| `unit_id` | `int` | `1` | Measurement unit ID |
| `unit_txt` | `str` | `''` | Unit name (required when `unit_id == 99`) |
| `quantity` | `float` | `0` | Quantity |
| `price` | `float` | `0` | Unit price |
| `status` | `int` | `1` | 1 = active, -1 = delete this item |
| `amount` | `float` | `0` | Total amount (typically `quantity * price`) |
| `bar_code` | `str` | `''` | Barcode or medicine registration number |
| `akciz_id` | `int` | `0` | Excise code ID (0 if not excise goods) |
| `vat_type` | `VATType` | `VATType.REGULAR` | VAT taxation type |
| `quantity_ext` | `float` | `0` | Auxiliary quantity |
| `wood_label` | `str` | `''` | Timber label number (wood category) |
| `wood_type_id` | `int` | `0` | Wood type ID (wood category) |

**Methods:**

- `to_xml() -> ET.Element` — serialize to XML
- `GoodsItem.from_xml(elem) -> GoodsItem` — parse from XML

---

### `WoodDocument`

A wood-origin document attached to a timber waybill.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Record ID (0 for new) |
| `doc_number` | `str` | `''` | Document number |
| `doc_date` | `datetime \| None` | `None` | Document issue date |
| `doc_description` | `str` | `''` | Document type/description |
| `status` | `int` | `1` | 1 = active, -1 = delete |

**Methods:**

- `to_xml() -> ET.Element` — serialize to XML
- `WoodDocument.from_xml(elem) -> WoodDocument` — parse from XML

---

### `SubWayBill`

Reference to a sub-waybill under a distribution waybill.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Sub-waybill ID |
| `waybill_number` | `str` | `''` | Sub-waybill number |

**Methods:**

- `SubWayBill.from_xml(elem) -> SubWayBill` — parse from XML

---

### `WayBillSaveResult`

Result returned by `WayBillClient.save_waybill()`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | `int` | — | 0 on success, negative on error |
| `waybill_id` | `int` | — | The saved waybill's ID |
| `goods_results` | `list[dict]` | `[]` | Per-item results with `id`, `error`, `name`, `status` keys |

**Properties:**

- `is_success -> bool` — `True` when `status == 0`

**Usage:**

```python
result = client.save_waybill(waybill)
if result.is_success:
    print(f'Saved as ID {result.waybill_id}')
    for item in result.goods_results:
        if item['error'] != 0:
            print(f'Item error: {item["name"]} -> {item["error"]}')
```

---

### `WayBillListItem`

Summary record from a waybill list query (`get_waybills`, `get_buyer_waybills`, etc.).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Waybill ID |
| `waybill_type` | `int` | `0` | Waybill type code |
| `create_date` | `str` | `''` | Creation date |
| `buyer_tin` | `str` | `''` | Buyer TIN |
| `buyer_name` | `str` | `''` | Buyer name |
| `seller_tin` | `str` | `''` | Seller TIN |
| `seller_name` | `str` | `''` | Seller name |
| `start_address` | `str` | `''` | Start address |
| `end_address` | `str` | `''` | End address |
| `driver_tin` | `str` | `''` | Driver TIN |
| `transport_cost` | `float` | `0` | Transport cost |
| `reception_info` | `str` | `''` | Sender info |
| `receiver_info` | `str` | `''` | Receiver info |
| `delivery_date` | `str` | `''` | Delivery date |
| `status` | `int` | `0` | Status code |
| `activate_date` | `str` | `''` | Activation date |
| `parent_id` | `str` | `''` | Parent waybill ID |
| `full_amount` | `float` | `0` | Total amount |
| `car_number` | `str` | `''` | Vehicle number |
| `waybill_number` | `str` | `''` | Waybill number |
| `close_date` | `str` | `''` | Close date |
| `s_user_id` | `int` | `0` | Service user ID |
| `begin_date` | `str` | `''` | Begin date |
| `comment` | `str` | `''` | Comment |
| `buyer_status` | `int` | `0` | Buyer business status |
| `seller_status` | `int` | `0` | Seller business status |
| `is_confirmed` | `int` | `0` | Confirmation status |

---

## Reference Data Models

These models are returned by reference data lookups.

### `ServiceUser`

A registered service user account.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Service user ID |
| `user_name` | `str` | Login username |
| `un_id` | `int` | Taxpayer unique number |
| `ip` | `str` | Whitelisted IP address |
| `name` | `str` | Object / store name |

### `AkcizCode`

Excise (akciz) commodity code.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Excise code ID |
| `title` | `str` | Full display title |
| `measurement` | `str` | Unit of measurement |
| `commodity_code` | `str` | Commodity code |
| `rate` | `float` | Excise tax rate |

### `WayBillTypeInfo`

Waybill type reference record.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Type ID |
| `name` | `str` | Type display name |

### `WayBillUnit`

Measurement unit reference record.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Unit ID |
| `name` | `str` | Unit display name |

### `TransportType`

Transport type reference record.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Transport type ID |
| `name` | `str` | Display name |

### `WoodType`

Wood/timber type reference record.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Wood type ID |
| `name` | `str` | Short name |
| `description` | `str` | Extended description |

### `ErrorCode`

API error code reference.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Numeric error code (negative) |
| `text` | `str` | Error description |
| `error_type` | `int` | 1 = waybill, 2 = goods item, 3 = invoice |

---

## Customs Models

### `CustomsAuthResponse`

Authentication response from the customs API.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `access_token` | `str` | `''` | Bearer token for subsequent requests |
| `status` | `int` | `0` | Response status code |
| `message` | `str` | `''` | Status message (or PIN token for 2FA) |

**Methods:**

- `CustomsAuthResponse.from_dict(data) -> CustomsAuthResponse` — parse from API JSON

---

### `CustomsDeclaration`

A single customs declaration record.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `declaration_number` | `str` | `''` | Unique declaration number |
| `assessment_date` | `str` | `''` | Date the declaration was assessed |
| `commodity_code` | `str` | `''` | HS commodity code |
| `description` | `str` | `''` | Goods description |
| `quantity` | `float` | `0` | Declared quantity |
| `net_weight` | `float` | `0` | Net weight in kg |
| `gross_weight` | `float` | `0` | Gross weight in kg |
| `statistical_value` | `float` | `0` | Statistical value |
| `customs_value` | `float` | `0` | Customs value |
| `duty_amount` | `float` | `0` | Customs duty amount |
| `vat_amount` | `float` | `0` | VAT amount |
| `excise_amount` | `float` | `0` | Excise tax amount |
| `country_of_origin` | `str` | `''` | Country of origin code |
| `country_of_dispatch` | `str` | `''` | Country of dispatch code |
| `raw_data` | `dict` | `{}` | Original dict for any unmapped fields |

**Methods:**

- `CustomsDeclaration.from_dict(data) -> CustomsDeclaration` — parse from API JSON

---

# Invoice Models

**Source:** `rsge/invoice/models.py`

## `InvoiceAuthResponse`

Authentication response from the eAPI.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `access_token` | `str` | `''` | Bearer token for subsequent requests |
| `pin_token` | `str` | `''` | Token for 2FA PIN verification (empty if one-factor) |
| `masked_mobile` | `str` | `''` | Masked phone number for PIN delivery |
| `expires_in` | `int` | `0` | Token expiry time in seconds |
| `status_id` | `int` | `0` | Response status ID (0 = success) |
| `status_text` | `str` | `''` | Response status message |

**Properties:**

- `needs_pin -> bool` — `True` when `pin_token` is set but `access_token` is empty (2FA required)

**Methods:**

- `InvoiceAuthResponse.from_dict(data) -> InvoiceAuthResponse` — parse from eAPI JSON

**Usage:**

```python
auth = client.authenticate('user', 'pass')
if auth.needs_pin:
    auth = client.authenticate_pin(auth.pin_token, input('PIN: '))
print(f'Token: {auth.access_token[:20]}...')
```

---

## `Invoice`

Main invoice/declaration document model. The primary model for creating, saving, and retrieving invoices.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Invoice ID (0 for new invoices) |
| `inv_serie` | `str` | `''` | Invoice serie |
| `inv_number` | `str` | `''` | Invoice number (OUT, assigned on activation) |
| `inv_category` | `int` | `0` | Invoice category code (see `InvoiceCategory`) |
| `inv_type` | `int` | `0` | Invoice type code (see `InvoiceType`) |
| `seller_action` | `int` | `0` | Seller action code (OUT) |
| `buyer_action` | `int` | `0` | Buyer action code (OUT) |
| `operation_date` | `str` | `''` | Operation date (`DD-MM-YYYY HH:MM:SS`) |
| `activate_date` | `str` | `''` | Activation date (OUT) |
| `create_date` | `str` | `''` | Creation date (OUT) |
| `correct_reason_id` | `int` | `0` | Correction reason ID (see `CorrectReason`) |
| `tin_seller` | `str` | `''` | Seller TIN |
| `tin_buyer` | `str` | `''` | Buyer TIN |
| `foreign_buyer` | `str` | `'false'` | Whether buyer is foreign |
| `name_seller` | `str` | `''` | Seller name (OUT) |
| `name_buyer` | `str` | `''` | Buyer name (OUT) |
| `amount_full` | `float` | `0` | Total amount |
| `amount_excise` | `float` | `0` | Total excise amount |
| `amount_vat` | `float` | `0` | Total VAT amount (OUT) |
| `trans_start_address` | `str` | `''` | Transport start address |
| `trans_end_address` | `str` | `''` | Transport end address |
| `trans_company_tin` | `str` | `''` | Transport company TIN |
| `trans_driver_tin` | `str` | `''` | Driver TIN |
| `trans_car_no` | `str` | `''` | Vehicle plate number |
| `trans_cost` | `str` | `''` | Transportation cost |
| `trans_cost_payer` | `int` | `0` | Cost payer (1=buyer, 2=seller) |
| `inv_comment` | `str` | `''` | Comment text |
| `parent_id` | `int \| None` | `None` | Parent invoice ID (for distribution) |
| `prev_correction_id` | `int` | `0` | Previous correction invoice ID |
| `template_name` | `str` | `''` | Template name |
| `invoice_goods` | `list[InvoiceGoods]` | `[]` | Line items |
| `invoice_return` | `list[InvoiceReturn]` | `[]` | Return references |
| `invoice_advance` | `list[InvoiceAdvance]` | `[]` | Advance payment references |
| `sub_invoices_distribution` | `list[SubInvoiceDistribution]` | `[]` | Distribution sub-invoices (OUT) |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |

> Fields marked **(OUT)** are read-only — set by the server and not sent on save.

**Methods:**

- `add_goods(goods_name, quantity, unit_price, **kwargs) -> InvoiceGoods` — add a goods item with auto-calculated `amount`
- `to_dict() -> dict` — serialize to eAPI JSON (writable fields only)
- `Invoice.from_dict(data) -> Invoice` — parse from eAPI JSON response

**Usage:**

```python
inv = Invoice(
    inv_category   = InvoiceCategory.GOODS_SERVICE,
    inv_type       = InvoiceType.WITH_TRANSPORT,
    operation_date = '10-04-2025 10:00:00',
    tin_seller     = '206322102',
    tin_buyer      = '12345678910',
)
inv.add_goods('Office Supplies', quantity=10, unit_price=25.50)
# inv.invoice_goods[0].amount == 255.0 (auto-calculated)
```

---

## `InvoiceGoods`

A single goods/service line item on an invoice.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Line item ID (0 for new) |
| `invoice_id` | `int` | `0` | Parent invoice ID |
| `goods_name` | `str` | `''` | Product / service description |
| `barcode` | `str` | `''` | Barcode value |
| `unit_id` | `int` | `0` | Measurement unit ID |
| `unit_txt` | `str` | `''` | Unit text (when `unit_id=99` "other") |
| `quantity` | `float` | `0` | Quantity |
| `quantity_ext` | `str` | `''` | Additional quantity |
| `unit_price` | `float` | `0` | Unit price |
| `amount` | `float` | `0` | Total amount (`quantity * unit_price`) |
| `vat_amount` | `float` | `0` | VAT amount (OUT) |
| `vat_type` | `int` | `0` | VAT type (0=standard, 1=zero, 2=exempt) |
| `excise_amount` | `float` | `0` | Excise tax amount |
| `excise_id` | `int` | `0` | Excise code ID |
| `excise_unit_price` | `float` | `0` | Excise unit price |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |

**Methods:**

- `to_dict() -> dict` — serialize to eAPI JSON
- `InvoiceGoods.from_dict(data) -> InvoiceGoods` — parse from eAPI JSON

---

## `InvoiceReturn`

Return reference on an invoice.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `return_invoice_id` | `int` | `0` | ID of the invoice being returned |
| `corrected_invoice_id` | `int` | `0` | Corrected invoice ID (OUT) |
| `inv_number` | `str` | `''` | Invoice number (OUT) |
| `buyer` | `str` | `''` | Buyer info (OUT) |
| `operation_date` | `str` | `''` | Operation date (OUT) |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |

**Methods:**

- `to_dict() -> dict` — serializes only `RETURN_INVOICE_ID`
- `InvoiceReturn.from_dict(data) -> InvoiceReturn` — parse from eAPI JSON

---

## `InvoiceAdvance`

Advance payment reference on an invoice.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `parent_invoice_id` | `int` | `0` | Parent invoice ID |
| `id` | `int` | `0` | Sub-document ID |
| `operation_date` | `str` | `''` | Operation date |
| `amount` | `float` | `0` | Advance amount |
| `inv_number` | `str` | `''` | Invoice number (OUT) |
| `amount_full` | `float` | `0` | Full amount (OUT) |
| `activate_date` | `str` | `''` | Activation date (OUT) |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |

**Methods:**

- `to_dict() -> dict` — serializes `ID`, `AMOUNT`, and optionally `OPERATION_DATE`
- `InvoiceAdvance.from_dict(data) -> InvoiceAdvance` — parse from eAPI JSON

---

## `SubInvoiceDistribution`

Distribution sub-invoice reference (read-only, OUT parameter).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `parent_invoice_id` | `int` | `0` | Parent invoice ID |
| `sub_invoice_id` | `int` | `0` | Sub-invoice ID |
| `inv_number` | `str` | `''` | Invoice number |
| `amount_full` | `float` | `0` | Full amount |
| `goods_amount_sum` | `float` | `0` | Goods total amount |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |

**Methods:**

- `SubInvoiceDistribution.from_dict(data) -> SubInvoiceDistribution` — parse from eAPI JSON

---

## `InvoiceAction`

Invoice status/action entry returned by `get_actions()`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int` | `0` | Status ID |
| `name` | `str` | `''` | Status name (Georgian) |
| `seller_action` | `int` | `0` | Seller action code |
| `buyer_action` | `int` | `0` | Buyer action code |

---

## `Unit`

Measurement unit from `get_units()`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `str` | `''` | Unit ID |
| `label` | `str` | `''` | Unit display label (e.g., "ცალი", "კგ") |

---

## `OrgInfo`

Organization info from `get_org_info()`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `tin` | `str` | `''` | Tax identification number |
| `address` | `str` | `''` | Registered address |
| `is_vat_payer` | `bool` | `False` | Whether the org is a VAT payer |
| `is_diplomat` | `bool` | `False` | Whether the org has diplomatic status |
| `name` | `str` | `''` | Organization name |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |

---

## `BarCode`

Barcode catalog entry.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `barcode` | `str` | `''` | Barcode value |
| `goods_name` | `str` | `''` | Product name |
| `unit_id` | `int` | `0` | Unit ID |
| `unit_txt` | `str` | `''` | Unit text |
| `vat_type` | `int` | `0` | VAT type |
| `unit_price` | `float` | `0` | Unit price |

---

## `TransactionResult`

Result from `get_transaction_result()` (async save polling).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `invoice_id` | `int` | `0` | Created/updated invoice ID |
| `raw_data` | `dict` | `{}` | Original dict for unmapped fields |
