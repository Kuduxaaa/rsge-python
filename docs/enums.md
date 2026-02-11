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

---

# Invoice Enums

Enums specific to the eAPI Invoice/Declaration service. Import them directly from `rsge`:

```python
from rsge import InvoiceCategory, InvoiceType, InvoiceVATType, InvoiceListType
```

**Source:** `rsge/invoice/enums.py`

---

## InvoiceCategory

საგადასახადო დოკუმენტის კატეგორია — Invoice document category.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `GOODS_SERVICE` | `1` | მინოდება/მომსახურება | Goods / service delivery |
| `WOOD` | `2` | ხე-ტყე | Wood / timber products |
| `PETROLEUM` | `3` | ნავთობპროდუქტები | Petroleum products |
| `ADVANCE` | `4` | ავანსი | Advance payment |

```python
inv = Invoice(inv_category=InvoiceCategory.GOODS_SERVICE)
```

---

## InvoiceType

საგადასახადო დოკუმენტის ტიპი — Invoice document type.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `INNER_TRANSPORT` | `1` | შიდა გადაზიდვა | Internal transfer |
| `WITH_TRANSPORT` | `2` | ტრანსპორტირებით | Delivery with transportation |
| `WITHOUT_TRANSPORT` | `3` | ტრანსპორტირების გარეშე | Delivery without transportation |
| `DISTRIBUTION` | `4` | დისტრიბუცია | Distribution |
| `RETURN` | `5` | უკან დაბრუნება | Return of goods |
| `ADVANCE` | `6` | ავანსი | Advance payment |
| `RETAIL` | `7` | საცალო მინოდებისთვის | For retail delivery |
| `WHOLESALE` | `8` | საბითუმო მინოდებისთვის | For wholesale delivery |
| `IMPORT_TRANSPORT` | `9` | იმპორტირებისას ტრანსპორტირება | Import: transport to customs destination |
| `EXPORT_TRANSPORT` | `10` | ექსპორტისას ტრანსპორტირება | Export: transport from customs origin |
| `SERVICE` | `11` | მომსახურება | Service provision |

```python
inv = Invoice(inv_type=InvoiceType.WITH_TRANSPORT)
```

---

## InvoiceVATType

დღგ-ს დაბეგვრის ტიპი — VAT taxation type for invoice goods.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `STANDARD` | `0` | ჩვეულებრივი | Standard / regular VAT |
| `ZERO_RATE` | `1` | ნულოვანი | Zero-rated |
| `EXEMPT` | `2` | დაუბეგრავი | VAT exempt |

> **Note:** This is separate from the waybill `VATType` to avoid cross-module coupling, though the values are the same.

---

## InvoiceListType

ListInvoices TYPE filter values.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `SELLER_DOCS` | `1` | გამორნერილი დოკუმენტები | Seller's own documents |
| `SELLER_DECL` | `10` | დეკლარაციებზე მისაბმელი | Seller's documents for declaration |
| `BUYER_DOCS` | `2` | თქვენზე გამორნერილი | Documents addressed to buyer |
| `BUYER_DECL` | `20` | მყიდველის დეკლარაცია | Buyer's documents for declaration |
| `SENT_TO_DECL` | `21` | გადამზიდავზე გამორნერილი | Sent for declaration |
| `TEMPLATES` | `3` | შაბლონები | Templates |
| `TEMPLATES_DECL` | `30` | შაბლონები დეკლარაციისთვის | Templates for declaration |
| `ADVANCE_WITH_BALANCE` | `5` | ავანსი ბალანსით | Advance documents with balance |
| `ADVANCE_BALANCE_DECL` | `50` | ავანსი ბალანსით (დეკლარაცია) | Advance balance for declarations |

```python
invoices = client.list_invoices(TYPE=InvoiceListType.SELLER_DOCS)
```

---

## CorrectReason

კორექტირების მიზეზი — Correction reason codes.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `NONE` | `0` | არ არის | No correction |
| `WRONG_AMOUNT` | `1` | არასწორი თანხა | Wrong amount |
| `WRONG_GOODS` | `2` | არასწორი სახე | Wrong goods/operation |
| `WRONG_TIN` | `3` | არასწორი TIN | Wrong TIN / compensation change |
| `WRONG_DATE` | `4` | არასწორი თარიღი | Wrong date / partial return |
| `WRONG_ADDRESS` | `5` | რედაქტირება | Wrong address |
| `OTHER` | `6` | სხვა | Other reason |

---

## ReturnType

უკან დაბრუნების ტიპი — Return type.

| Member | Value | Georgian | Description |
|--------|-------|----------|-------------|
| `PARTIAL` | `0` | ნაწილობრივი | Partial return |
| `FULL` | `1` | სრული | Full return |
