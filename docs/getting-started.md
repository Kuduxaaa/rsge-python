# Getting Started

## Requirements

- Python 3.10 or later
- RS.ge service credentials (service username + password) from the [RS.ge declarant portal](https://eservices.rs.ge)

## Installation

```bash
pip install rsge-sdk
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

## Quickstart: WayBill Client

```python
from rsge import WayBillClient, WayBillType

with WayBillClient('your_service_user', 'your_service_password') as client:
    un_id, s_user_id = client.check_service_user()
    print(f'Authenticated: un_id={un_id}, s_user_id={s_user_id}')

    waybill = client.create_waybill(
        waybill_type  = WayBillType.TRANSPORTATION,
        buyer_tin     = '12345678901',
        start_address = 'Tbilisi, Rustaveli Ave 1',
        end_address   = 'Batumi, Chavchavadze St 5',
        driver_tin    = '01234567890',
        car_number    = 'AB-123-CD',
    )

    waybill.add_goods(
        name     = 'Office Supplies',
        unit_id  = 1,
        quantity = 10,
        price    = 25.50,
        bar_code = '5901234123457',
    )

    result = client.save_waybill(waybill)
    if result.is_success:
        print(f'Saved waybill ID: {result.waybill_id}')
        number = client.activate_waybill(result.waybill_id)
        print(f'Activated: {number}')
```

## Quickstart: Customs Client

```python
from rsge import CustomsClient

with CustomsClient() as client:
    auth = client.authenticate('your_username', 'your_password')
    print(f'Token: {auth.access_token[:20]}...')

    declarations = client.get_declarations(
        date_from = '2024-01-01',
        date_to   = '2024-01-31',
    )

    for decl in declarations:
        print(f'{decl.declaration_number}: {decl.description}')
```

## Next Steps

- [WayBill Client API Reference](waybill-client.md) — full method reference with usage examples
- [Customs Client API Reference](customs-client.md) — authentication flows and declaration queries
- [Models Reference](models.md) — all dataclass models with field descriptions
- [Enums Reference](enums.md) — waybill types, statuses, and other enum values
- [Exceptions Reference](exceptions.md) — error handling patterns
- `examples/` directory — 10 standalone example scripts covering all major workflows
