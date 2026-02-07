# Enums Reference

All enums are `IntEnum` subclasses, so they work as both integers and named constants. Import them directly from `rsge`:

```python
from rsge import WayBillType, WayBillStatus, TransportationType, VATType
```

**Source:** `rsge/waybill/enums.py`

---

## WayBillType

Types of electronic commodity waybills.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `INNER_TRANSPORT` | `1` | შიდა გადაზიდვა | Internal transfer within the same entity |
| `TRANSPORTATION` | `2` | მიწოდება ტრანსპორტირებით | Delivery with transportation |
| `WITHOUT_TRANSPORTATION` | `3` | მიწოდება ტრანსპორტირების გარეშე | Delivery without transportation |
| `DISTRIBUTION` | `4` | დისტრიბუცია | Distribution (includes main + sub-waybills) |
| `RETURN` | `5` | საქონლის უკან დაბრუნება | Goods return |
| `SUB_WAYBILL` | `6` | ქვე-ზედნადები | Sub-waybill (child of a distribution waybill) |

```python
waybill = client.create_waybill(waybill_type=WayBillType.TRANSPORTATION)
```

---

## WayBillStatus

Lifecycle status of a waybill.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `SAVED` | `0` | შენახული | Saved / draft |
| `ACTIVE` | `1` | აქტიური / აქტივირებული | Activated, transportation started |
| `COMPLETED` | `2` | დასრულებული | Completed, goods delivered |
| `SENT_TO_TRANSPORTER` | `8` | გადამზიდავთან გადაგზავნილი | Forwarded to transporter company |
| `DELETED` | `-1` | წაშლილი | Deleted |
| `CANCELLED` | `-2` | გაუქმებული | Cancelled / voided |

```python
if wb.status == WayBillStatus.ACTIVE:
    client.close_waybill(wb.id)
```

---

## TransportationType

Type of transport used for delivery.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `TRUCK` | `1` | სატვირთო მანქანა | Truck / cargo vehicle |
| `VEHICLE` | `2` | მსუბუქი ავტომობილი | Light vehicle |
| `RAILWAY` | `3` | რკინიგზა | Railway transport |
| `OTHER` | `4` | სხვა | Other (requires `transport_type_txt` to be filled) |

---

## VATType

VAT taxation type for goods items.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `REGULAR` | `0` | ჩვეულებრივი | Regular / standard VAT |
| `ZERO_RATE` | `1` | ნულოვანი | Zero-rated |
| `EXEMPT` | `2` | დაუბეგრავი | VAT exempt |

```python
waybill.add_goods(
    name     = 'Exported Goods',
    unit_id  = 1,
    quantity = 100,
    price    = 5.0,
    bar_code = '1234567890',
    vat_type = VATType.ZERO_RATE,
)
```

---

## CategoryType

Waybill category.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `REGULAR` | `0` | ჩვეულებრივი | Standard goods |
| `WOOD` | `1` | ხე-ტყე | Wood / timber (requires additional wood fields) |

---

## TransportCostPayer

Who pays the transportation cost.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `BUYER` | `1` | მყიდველი | Buyer pays |
| `SELLER` | `2` | გამყიდველი | Seller pays |

---

## ConfirmationStatus

Buyer confirmation status for waybill filtering.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `UNCONFIRMED` | `0` | დაუდასტურებელი | Not yet confirmed |
| `CONFIRMED` | `1` | დადასტურებული | Confirmed / accepted |
| `REJECTED` | `-1` | უარყოფილი | Rejected by buyer |

Used with `get_waybills_ex()` and `get_buyer_waybills_ex()`:

```python
confirmed = client.get_waybills_ex(is_confirmed=ConfirmationStatus.CONFIRMED)
```

---

## BusinessStatus

Taxpayer business status.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `NONE` | `0` | სტატუსის გარეშე | No special status |
| `MICRO` | `1` | მიკრო ბიზნესის სტატუსი | Micro business |
| `SMALL` | `2` | მცირე ბიზნესის სტატუსი | Small business |

---

## CustomsConfirmStatus

Customs checkpoint confirmation status.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `CONFIRMED` | `1` | დადასტურებული | Confirmed by customs |
| `REJECTED` | `2` | უარყოფილი | Rejected by customs |
