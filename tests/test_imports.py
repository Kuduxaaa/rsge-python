"""Verify that all public API symbols are importable."""


def test_version():
    from rsge import __version__
    assert __version__


def test_waybill_client_importable():
    from rsge import WayBillClient
    assert WayBillClient


def test_customs_client_importable():
    from rsge import CustomsClient
    assert CustomsClient


def test_invoice_client_importable():
    from rsge import InvoiceClient
    assert InvoiceClient


def test_enums_importable():
    from rsge import (
        BusinessStatus,
        CategoryType,
        ConfirmationStatus,
        TransportationType,
        TransportCostPayer,
        VATType,
        WayBillStatus,
        WayBillType,
    )
    assert WayBillType.TRANSPORTATION == 2
    assert WayBillStatus.ACTIVE == 1
    assert BusinessStatus.NONE == 0
    assert CategoryType.REGULAR == 0
    assert ConfirmationStatus.UNCONFIRMED == 0
    assert TransportationType.TRUCK == 1
    assert TransportCostPayer.BUYER == 1
    assert VATType.REGULAR == 0


def test_invoice_enums_importable():
    from rsge import (
        CorrectReason,
        InvoiceCategory,
        InvoiceListType,
        InvoiceType,
        InvoiceVATType,
        ReturnType,
    )
    assert InvoiceCategory.GOODS_SERVICE == 1
    assert InvoiceType.WITH_TRANSPORT == 2
    assert InvoiceVATType.STANDARD == 0
    assert InvoiceListType.SELLER_DOCS == 1
    assert CorrectReason.NONE == 0
    assert ReturnType.PARTIAL == 0


def test_invoice_models_importable():
    from rsge import (
        BarCode,
        Invoice,
        InvoiceAction,
        InvoiceAdvance,
        InvoiceAuthResponse,
        InvoiceGoods,
        InvoiceReturn,
        OrgInfo,
        SubInvoiceDistribution,
        TransactionResult,
        Unit,
    )
    assert Invoice
    assert InvoiceGoods
    assert InvoiceReturn
    assert InvoiceAdvance
    assert SubInvoiceDistribution
    assert InvoiceAction
    assert InvoiceAuthResponse
    assert Unit
    assert OrgInfo
    assert BarCode
    assert TransactionResult


def test_models_importable():
    from rsge import CustomsDeclaration, GoodsItem, WayBill, WayBillSaveResult
    assert WayBill
    assert GoodsItem
    assert WayBillSaveResult
    assert CustomsDeclaration


def test_exceptions_importable():
    from rsge import (
        RSGeAPIError,
        RSGeAuthenticationError,
        RSGeConnectionError,
        RSGeError,
        RSGeValidationError,
    )
    assert issubclass(RSGeAuthenticationError, RSGeError)
    assert issubclass(RSGeValidationError, RSGeError)
    assert issubclass(RSGeAPIError, RSGeError)
    assert issubclass(RSGeConnectionError, RSGeError)
