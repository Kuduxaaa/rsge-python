"""Enumeration types for the RS.ge eAPI Invoice/Declaration service.

These enums map the numeric codes used by the eAPI to
human-readable names, preventing magic-number usage throughout
the codebase.
"""

from __future__ import annotations

from enum import IntEnum


class InvoiceCategory(IntEnum):
    """საგადასახადო დოკუმენტის კატეგორია."""

    GOODS_SERVICE = 1
    """
    მინოდება/მომსახურება - Goods / service delivery.
    """

    WOOD = 2
    """
    ხე-ტყე - Wood / timber products.
    """

    PETROLEUM = 3
    """
    ნავთობპროდუქტები - Petroleum products.
    """

    ADVANCE = 4
    """
    ავანსი - Advance payment.
    """


class InvoiceType(IntEnum):
    """საგადასახადო დოკუმენტის ტიპი."""

    INNER_TRANSPORT = 1
    """
    შიდა გადაზიდვა - Internal transfer.
    """

    WITH_TRANSPORT = 2
    """
    ტრანსპორტირებით - Delivery with transportation.
    """

    WITHOUT_TRANSPORT = 3
    """
    ტრანსპორტირების გარეშე - Delivery without transportation.
    """

    DISTRIBUTION = 4
    """
    დისტრიბუცია - Distribution.
    """

    RETURN = 5
    """
    უკან დაბრუნება - Return of goods.
    """

    ADVANCE = 6
    """
    ავანსი - Advance payment.
    """

    RETAIL = 7
    """
    საცალო მინოდებისთვის - For retail delivery.
    """

    WHOLESALE = 8
    """
    საბითუმო მინოდებისთვის - For wholesale delivery.
    """

    IMPORT_TRANSPORT = 9
    """
    იმპორტირებისას დასანაყობების ადგილამდე ტრანსპორტირებისათვის
    - Import: transport to customs destination.
    """

    EXPORT_TRANSPORT = 10
    """
    ექსპორტისას დასანაყობების ადგილიდან ტრანსპორტირებისათვის
    - Export: transport from customs origin.
    """

    SERVICE = 11
    """
    მომსახურება - Service provision.
    """


class InvoiceVATType(IntEnum):
    """დღგ-ს დაბეგვრის ტიპი (eAPI invoice-specific)."""

    STANDARD = 0
    """
    ჩვეულებრივი - Standard / regular VAT.
    """

    ZERO_RATE = 1
    """
    ნულოვანი - Zero-rated.
    """

    EXEMPT = 2
    """
    დაუბეგრავი - VAT exempt.
    """


class InvoiceListType(IntEnum):
    """ListInvoices TYPE ფილტრის მნიშვნელობები."""

    SELLER_DOCS = 1
    """
    თქვენს მიერ გამორნერილი დოკუმენტები - Seller's own documents.
    """

    SELLER_DECL = 10
    """
    თქვენს მიერ გამორნერილი დეკლარაციებზე მისაბმელი დოკუმენტები
    - Seller's documents for declaration binding.
    """

    BUYER_DOCS = 2
    """
    თქვენზე გამორნერილი დოკუმენტები - Documents addressed to you (buyer).
    """

    BUYER_DECL = 20
    """
    თქვენზე გამორნერილი დეკლარაციებზე მისაბმელი დოკუმენტები
    - Buyer's documents for declaration binding.
    """

    SENT_TO_DECL = 21
    """
    თქვენზე როგორც გადამზიდავზე გამორნერილი დოკუმენტები
    - Documents sent for declaration.
    """

    TEMPLATES = 3
    """
    თქვენზე როგორც გადამბიძდავზე გამორნერილი დოკუმენტები - Templates.
    """

    TEMPLATES_DECL = 30
    """
    შაბლონები - Templates for declaration.
    """

    ADVANCE_WITH_BALANCE = 5
    """
    ავანსის დოკუმენტები დარჩენილი ბალანსით - Advance documents with balance.
    """

    ADVANCE_BALANCE_DECL = 50
    """
    ავანსის დოკუმენტები დარჩენილი ბალანსით გირჩევთ გამოიყენოთ ორნიშნა კოდები
    - Advance balance for declarations.
    """


class CorrectReason(IntEnum):
    """კორექტირების მიზეზი."""

    NONE = 0
    """
    არ არის - No correction.
    """

    WRONG_AMOUNT = 1
    """
    გაუქმებულია დასაბეგრი ოპერაციის თანხა - Wrong amount.
    """

    WRONG_GOODS = 2
    """
    შეცვლილია დასაბეგრი ოპერაციის სახე - Wrong goods/operation.
    """

    WRONG_TIN = 3
    """
    ფასების შემცირების ან სხვა მიზეზით შეცვლილია ოპერაციაზე
    ადრე შეთანხმებული კომპენსაციის თანხა - Wrong TIN.
    """

    WRONG_DATE = 4
    """
    საქონელი ან ნაწილობრივ უბრუნდება გამყიდველს - Wrong date.
    """

    WRONG_ADDRESS = 5
    """
    რედაქტირება - Wrong address.
    """

    OTHER = 6
    """
    სხვა - Other reason.
    """


class ReturnType(IntEnum):
    """უკან დაბრუნების ტიპი."""

    PARTIAL = 0
    """
    ნაწილობრივი - Partial return.
    """

    FULL = 1
    """
    სრული - Full return.
    """
