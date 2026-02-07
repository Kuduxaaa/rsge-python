"""
Enumeration types for the RS.ge WayBill service.

These enums map the numeric codes used by the RS.ge API to
human-readable names, preventing magic-number usage throughout
the codebase.
"""

from __future__ import annotations

from enum import IntEnum


class WayBillType(IntEnum):
    """
    Types of electronic commodity waybills.
    """

    INNER_TRANSPORT = 1
    """
    შიდა გადაზიდვა - Internal transfer within the same entity.
    """

    TRANSPORTATION = 2
    """
    მიწოდება ტრანსპორტირებით - Delivery with transportation.
    """

    WITHOUT_TRANSPORTATION = 3
    """
    მიწოდება ტრანსპორტირების გარეშე - Delivery without transportation.
    """

    DISTRIBUTION = 4
    """
    დისტრიბუცია - Distribution (includes main + sub-waybills).
    """

    RETURN = 5
    """
    საქონლის უკან დაბრუნება - Goods return.
    """

    SUB_WAYBILL = 6
    """
    ქვე-ზედნადები - Sub-waybill (child of a distribution waybill).
    """


class WayBillStatus(IntEnum):
    """
    Lifecycle status of a waybill.
    """

    SAVED = 0
    """
    შენახული - Saved / draft.
    """

    ACTIVE = 1
    """
    აქტიური / აქტივირებული - Activated, transportation started.
    """

    COMPLETED = 2
    """
    დასრულებული - Completed, goods delivered.
    """

    SENT_TO_TRANSPORTER = 8
    """
    გადამზიდავთან გადაგზავნილი - Forwarded to transporter company.
    """

    DELETED = -1
    """
    წაშლილი - Deleted.
    """

    CANCELLED = -2
    """
    გაუქმებული - Cancelled / voided.
    """


class TransportationType(IntEnum):
    """
    Type of transport used for delivery.
    """

    TRUCK = 1
    """
    სატვირთო მანქანა - Truck / cargo vehicle.
    """

    VEHICLE = 2
    """
    მსუბუქი ავტომობილი - Light vehicle.
    """

    RAILWAY = 3
    """
    რკინიგზა - Railway transport.
    """

    OTHER = 4
    """
    სხვა - Other (requires TRANS_TXT to be filled).
    """


class VATType(IntEnum):
    """
    VAT taxation type for goods items.
    """

    REGULAR = 0
    """
    ჩვეულებრივი - Regular / standard VAT.
    """

    ZERO_RATE = 1
    """
    ნულოვანი - Zero-rated.
    """

    EXEMPT = 2
    """
    დაუბეგრავი - VAT exempt.
    """


class CategoryType(IntEnum):
    """
    Waybill category.
    """

    REGULAR = 0
    """
    ჩვეულებრივი - Standard goods.
    """

    WOOD = 1
    """
    ხე-ტყე - Wood / timber (requires additional fields).
    """


class TransportCostPayer(IntEnum):
    """
    Who pays the transportation cost.
    """

    BUYER = 1
    """
    მყიდველი - Buyer pays.
    """

    SELLER = 2
    """
    გამყიდველი - Seller pays.
    """


class ConfirmationStatus(IntEnum):
    """
    Buyer confirmation status for waybill filtering.
    """

    UNCONFIRMED = 0
    """
    დაუდასტურებელი - Not yet confirmed.
    """

    CONFIRMED = 1
    """
    დადასტურებული - Confirmed / accepted.
    """

    REJECTED = -1
    """
    უარყოფილი - Rejected by buyer.
    """


class BusinessStatus(IntEnum):
    """
    Taxpayer business status.
    """

    NONE = 0
    """
    სტატუსის გარეშე - No special status.
    """

    MICRO = 1
    """
    მიკრო ბიზნესის სტატუსი - Micro business.
    """

    SMALL = 2
    """
    მცირე ბიზნესის სტატუსი - Small business.
    """


class CustomsConfirmStatus(IntEnum):
    """
    Customs checkpoint confirmation status.
    """

    CONFIRMED = 1
    """
    დადასტურებული - Confirmed by customs.
    """

    REJECTED = 2
    """
    უარყოფილი - Rejected by customs.
    """
