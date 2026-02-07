# Models Reference

All models are Python dataclasses that serialize to/from XML (waybill models) or JSON (customs models) for communication with the RS.ge APIs. Import them directly from `rsge`:

```python
from rsge import WayBill, GoodsItem, WayBillSaveResult, CustomsDeclaration
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
