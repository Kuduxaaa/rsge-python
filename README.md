# RS.ge Python SDK

Python SDK for the **Georgian Revenue Service** (სსიპ შემოსავლების სამსახური) electronic services, providing complete integration with:

- **WayBill Service** (ელექტრონული ზედნადები) — SOAP/XML API for electronic commodity waybills
- **Customs Declarations** (საბაჟო დეკლარაციები) — REST/JSON API for customs declaration data

## Installation

```bash
pip install rsge-sdk
```

Or install from source:

```bash
git clone https://github.com/kuduxaaa/rsge-sdk.git
cd rsge-sdk
pip install -e ".[dev]"
```

## Quick Start

### WayBill Service

```python
from rsge import WayBillClient, WayBillType, VATType

# Initialize client (test credentials from RS.ge documentation)
client = WayBillClient(
    service_user="tbilisi",
    service_password="123456",
)

# Verify credentials
un_id, s_user_id = client.check_service_user()
print(f"Taxpayer ID: {un_id}, User ID: {s_user_id}")

# Create a waybill
waybill = client.create_waybill(
    waybill_type=WayBillType.TRANSPORTATION,
    buyer_tin="12345678910",
    buyer_name="გიორგი გიორგაძე",
    start_address="თბილისი, საბურთალოს ქუჩა",
    end_address="თბილისი, გულუას ქუჩა",
    driver_tin="11111111111",
    driver_name="ბახვა ხორავა",
    car_number="AAA555",
)

# Add goods items
waybill.add_goods(
    name="შაქარი",
    unit_id=2,          # kg
    quantity=1000,
    price=1.0,
    bar_code="001",
    vat_type=VATType.REGULAR,
)

# Save to RS.ge
result = client.save_waybill(waybill)
if result.is_success:
    print(f"Waybill saved! ID: {result.waybill_id}")

    # Activate (start transport)
    wb_number = client.activate_waybill(result.waybill_id)
    print(f"Waybill number: {wb_number}")

    # Close (complete delivery)
    client.close_waybill(result.waybill_id)
```

### Customs Declarations

```python
from rsge import CustomsClient

client = CustomsClient()
client.authenticate("username", "password")

declarations = client.get_declarations(
    date_from="2024-01-01",
    date_to="2024-01-31",
)

for decl in declarations:
    print(f"{decl.declaration_number}: {decl.description} = {decl.customs_value}")

client.sign_out()
```

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Installation, requirements, quickstart examples |
| [WayBill Client](docs/waybill-client.md) | Full WayBillClient API reference (40+ methods) |
| [Customs Client](docs/customs-client.md) | CustomsClient API reference (auth flows, declarations) |
| [Models](docs/models.md) | All dataclass models with fields and types |
| [Enums](docs/enums.md) | All enum types with values and Georgian descriptions |
| [Exceptions](docs/exceptions.md) | Exception hierarchy and error handling patterns |

## API Reference

### WayBillClient Methods

| Method | Description |
|--------|-------------|
| `check_service_user()` | Verify credentials, get `(un_id, s_user_id)` |
| `update_service_user()` | Update service user registration |
| `get_service_users()` | List service users |
| **Reference Data** | |
| `get_akciz_codes()` | Excise commodity codes |
| `get_waybill_types()` | Waybill type reference |
| `get_waybill_units()` | Measurement units |
| `get_transport_types()` | Transportation types |
| `get_wood_types()` | Wood/timber types |
| `get_error_codes()` | Error code reference |
| `get_name_from_tin(tin)` | Look up name by TIN |
| **Waybill CRUD** | |
| `create_waybill(...)` | Create waybill in memory |
| `save_waybill(waybill)` | Save/update on server |
| `get_waybill(id)` | Retrieve single waybill |
| `get_waybills(...)` | List seller-side waybills |
| `get_buyer_waybills(...)` | List buyer-side waybills |
| `get_waybills_ex(...)` | Extended seller list with confirmation filter |
| `get_buyer_waybills_ex(...)` | Extended buyer list |
| `get_waybills_v1(...)` | List by last-update date (max 3 days) |
| **Lifecycle** | |
| `activate_waybill(id)` | Start transportation |
| `activate_waybill_with_date(id, date)` | Activate with specific date |
| `close_waybill(id)` | Complete delivery |
| `close_waybill_with_date(id, date)` | Close with delivery date |
| `delete_waybill(id)` | Delete saved waybill |
| `cancel_waybill(id)` | Cancel activated waybill |
| `confirm_waybill(id)` | Buyer confirms |
| `reject_waybill(id)` | Buyer rejects |
| **Transporter** | |
| `save_waybill_transporter(...)` | Fill transporter fields |
| `activate_waybill_transporter(...)` | Activate as transporter |
| `close_waybill_transporter(...)` | Close as transporter |
| **Invoice** | |
| `save_invoice(waybill_id)` | Issue tax invoice from waybill |
| **Templates & Catalog** | |
| `save_waybill_template(name, wb)` | Save reusable template |
| `get_waybill_templates()` | List templates |
| `save_bar_code(...)` | Add to barcode catalog |
| `save_car_number(number)` | Register vehicle |

### WayBill Types

| Type | Value | Description |
|------|-------|-------------|
| `INNER_TRANSPORT` | 1 | Internal transfer |
| `TRANSPORTATION` | 2 | Delivery with transport |
| `WITHOUT_TRANSPORTATION` | 3 | Delivery without transport |
| `DISTRIBUTION` | 4 | Distribution (main + sub-waybills) |
| `RETURN` | 5 | Goods return |
| `SUB_WAYBILL` | 6 | Sub-waybill (child of distribution) |

### Status Codes

| Status | Value | Description |
|--------|-------|-------------|
| `SAVED` | 0 | Draft |
| `ACTIVE` | 1 | Transportation started |
| `COMPLETED` | 2 | Delivered |
| `SENT_TO_TRANSPORTER` | 8 | Forwarded to carrier |
| `DELETED` | -1 | Deleted |
| `CANCELLED` | -2 | Voided |

## Project Structure

```
rsge/
├── __init__.py              # Public API exports
├── core/
│   ├── exceptions.py        # Exception hierarchy
│   ├── transport.py         # SOAP HTTP transport
│   └── xml_utils.py         # XML builder/parser helpers
├── waybill/
│   ├── client.py            # WayBillClient (main entry point)
│   ├── enums.py             # WayBillType, Status, etc.
│   └── models.py            # WayBill, GoodsItem, etc.
└── customs/
    ├── client.py            # CustomsClient (REST API)
    └── models.py            # CustomsDeclaration, etc.
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## Test Credentials

From the official RS.ge documentation:

| | Account 1 | Account 2 |
|---|-----------|-----------|
| **User** | `tbilisi` | `satesto2` |
| **Password** | `123456` | `123456` |
| **TIN** | `206322102` | `12345678910` |

## License

MIT