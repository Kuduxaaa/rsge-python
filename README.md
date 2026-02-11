# RS.ge Python SDK

[![PyPI version](https://img.shields.io/pypi/v/rsge-python.svg)](https://pypi.org/project/rsge-python/)
[![PyPI downloads](https://img.shields.io/pypi/dm/rsge-python.svg)](https://pypi.org/project/rsge-python/)
[![Python](https://img.shields.io/pypi/pyversions/rsge-python.svg)](https://pypi.org/project/rsge-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/kuduxaaa/rsge-python/actions/workflows/ci.yml/badge.svg)](https://github.com/kuduxaaa/rsge-python/actions/workflows/ci.yml)

Python SDK for the **Georgian Revenue Service** (სსიპ შემოსავლების სამსახური) electronic services.

- **WayBill Service** (ელექტრონული ზედნადები) — SOAP/XML API for electronic commodity waybills
- **Customs Declarations** (საბაჟო დეკლარაციები) — REST/JSON API for customs declaration data
- **Invoice / Declaration** (საგადასახადო დოკუმენტი) — REST/JSON API for tax invoices and declarations

## Installation

```bash
pip install rsge-python
```

Or install from source:

```bash
git clone https://github.com/kuduxaaa/rsge-python.git
cd rsge-python
pip install -e .
```

For development (includes pytest, ruff, mypy):

```bash
pip install -e ".[dev]"
```

**Requirements:** Python 3.10+

## Quick Start

### WayBill Service

```python
from rsge import WayBillClient, WayBillType, VATType

with WayBillClient('your_service_user', 'your_service_password') as client:
    # Verify credentials
    un_id, s_user_id = client.check_service_user()
    print(f'Taxpayer ID: {un_id}, User ID: {s_user_id}')

    # Create a waybill
    waybill = client.create_waybill(
        waybill_type  = WayBillType.TRANSPORTATION,
        buyer_tin     = '12345678901',
        start_address = 'Tbilisi, Rustaveli Ave 1',
        end_address   = 'Batumi, Chavchavadze St 5',
        driver_tin    = '01234567890',
        car_number    = 'AB-123-CD',
    )

    # Add goods
    waybill.add_goods(
        name     = 'Office Supplies',
        unit_id  = 1,
        quantity = 10,
        price    = 25.50,
        bar_code = '5901234123457',
        vat_type = VATType.REGULAR,
    )

    # Save, activate, close
    result = client.save_waybill(waybill)
    if result.is_success:
        wb_number = client.activate_waybill(result.waybill_id)
        print(f'Waybill number: {wb_number}')
        client.close_waybill(result.waybill_id)
```

### Customs Declarations

```python
from rsge import CustomsClient

with CustomsClient() as client:
    auth = client.authenticate('username', 'password')

    declarations = client.get_declarations(
        date_from = '2024-01-01',
        date_to   = '2024-01-31',
    )

    for decl in declarations:
        print(f'{decl.declaration_number}: {decl.description} = {decl.customs_value}')
```

### Invoice / Declaration Service

```python
from rsge import InvoiceClient, Invoice, InvoiceCategory, InvoiceType

with InvoiceClient() as client:
    # Authenticate (supports 2FA)
    auth = client.authenticate('your_username', 'your_password')

    if auth.needs_pin:
        pin = input('Enter PIN: ')
        auth = client.authenticate_pin(auth.pin_token, pin)

    # Create and save an invoice
    inv = Invoice(
        inv_category   = InvoiceCategory.GOODS_SERVICE,
        inv_type       = InvoiceType.WITH_TRANSPORT,
        operation_date = '10-04-2025 10:00:00',
        tin_seller     = '206322102',
        tin_buyer      = '12345678910',
    )

    inv.add_goods('Office Supplies', quantity=10, unit_price=25.50)
    inv.add_goods('Printer Paper',   quantity=5,  unit_price=15.00)

    txn_id = client.save_invoice(inv)
    result = client.get_transaction_result(txn_id)
    print(f'Saved invoice ID: {result.invoice_id}')

    # List, activate, and manage invoices
    invoices = client.list_invoices(TYPE=1, MAXIMUM_ROWS=20)
    client.activate_invoices([result.invoice_id])

    # Look up organization info
    org = client.get_org_info('206322102')
    print(f'{org.name} — VAT payer: {org.is_vat_payer}')
```

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Installation, requirements, quickstart examples |
| [WayBill Client](docs/waybill-client.md) | Full WayBillClient API reference (40+ methods) |
| [Customs Client](docs/customs-client.md) | CustomsClient API reference (auth flows, declarations) |
| [Invoice Client](docs/invoice-client.md) | InvoiceClient API reference (25+ methods, 2FA auth) |
| [Models](docs/models.md) | All dataclass models with fields and types |
| [Enums](docs/enums.md) | All enum types with values and Georgian descriptions |
| [Exceptions](docs/exceptions.md) | Exception hierarchy and error handling patterns |

## API Overview

### WayBillClient

| Category | Methods |
|----------|---------|
| **Auth** | `check_service_user()`, `get_service_users()`, `update_service_user()` |
| **CRUD** | `create_waybill()`, `save_waybill()`, `get_waybill()`, `get_waybills()`, `get_buyer_waybills()` |
| **Lifecycle** | `activate_waybill()`, `close_waybill()`, `delete_waybill()`, `cancel_waybill()` |
| **Buyer** | `confirm_waybill()`, `reject_waybill()` |
| **Transporter** | `save_waybill_transporter()`, `activate_waybill_transporter()`, `close_waybill_transporter()` |
| **Invoice** | `save_invoice()` |
| **Templates** | `save_waybill_template()`, `get_waybill_templates()`, `get_waybill_template()`, `delete_waybill_template()` |
| **Catalog** | `save_bar_code()`, `delete_bar_code()`, `get_bar_codes()` |
| **Vehicles** | `save_car_number()`, `delete_car_number()`, `get_car_numbers()` |
| **Reference** | `get_akciz_codes()`, `get_waybill_types()`, `get_waybill_units()`, `get_transport_types()`, `get_wood_types()`, `get_error_codes()`, `get_name_from_tin()` |

### CustomsClient

| Method | Description |
|--------|-------------|
| `authenticate()` | One-factor login |
| `authenticate_pin()` | Two-factor PIN verification |
| `get_declarations()` | Retrieve assessed declarations by date range |
| `sign_out()` | Invalidate token |

### InvoiceClient

| Category | Methods |
|----------|---------|
| **Auth** | `authenticate()`, `authenticate_pin()`, `sign_out()` |
| **Common** | `get_vat_payer_status()`, `get_org_info()`, `get_units()`, `get_transaction_result()` |
| **CRUD** | `get_invoice()`, `save_invoice()`, `list_invoices()`, `list_goods()` |
| **Lifecycle** | `activate_invoice()`, `activate_invoices()`, `delete_invoice()`, `cancel_invoice()` |
| **Buyer** | `confirm_invoice()`, `confirm_invoices()`, `refuse_invoice()`, `refuse_invoices()` |
| **Barcode** | `list_bar_codes()`, `get_bar_code()`, `clear_bar_codes()` |
| **Declaration** | `get_seq_num()`, `create_decl()`, `list_excise()` |

### WayBill Types & Statuses

| Type | Value | | Status | Value |
|------|-------|-|--------|-------|
| `INNER_TRANSPORT` | 1 | | `SAVED` | 0 |
| `TRANSPORTATION` | 2 | | `ACTIVE` | 1 |
| `WITHOUT_TRANSPORTATION` | 3 | | `COMPLETED` | 2 |
| `DISTRIBUTION` | 4 | | `SENT_TO_TRANSPORTER` | 8 |
| `RETURN` | 5 | | `DELETED` | -1 |
| `SUB_WAYBILL` | 6 | | `CANCELLED` | -2 |

## Error Handling

```python
from rsge import RSGeError, RSGeAuthenticationError, RSGeAPIError, RSGeConnectionError

try:
    result = client.save_waybill(waybill)
except RSGeAuthenticationError:
    print('Invalid credentials')
except RSGeConnectionError:
    print('Cannot reach RS.ge servers')
except RSGeAPIError as exc:
    print(f'API error {exc.code}: {exc.message}')
except RSGeError as exc:
    print(f'SDK error: {exc.message}')
```

## Project Structure

```
rsge/
├── __init__.py              # Public API exports
├── core/
│   ├── exceptions.py        # Exception hierarchy
│   ├── transport.py         # SOAP HTTP transport
│   └── xml_utils.py         # XML builder/parser helpers
├── waybill/
│   ├── client.py            # WayBillClient
│   ├── enums.py             # WayBillType, Status, etc.
│   └── models.py            # WayBill, GoodsItem, etc.
├── customs/
│   ├── client.py            # CustomsClient
│   └── models.py            # CustomsDeclaration, etc.
└── invoice/
    ├── client.py            # InvoiceClient (eAPI REST)
    ├── enums.py             # InvoiceCategory, InvoiceType, etc.
    └── models.py            # Invoice, InvoiceGoods, etc.
```

## Contributing

```bash
git clone https://github.com/kuduxaaa/rsge-python.git
cd rsge-python
pip install -e ".[dev]"
pytest
ruff check .
mypy rsge
```

## License

[MIT](LICENSE)
