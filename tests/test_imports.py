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


def test_enums_importable():
    from rsge import (
        WayBillType,
        WayBillStatus,
        TransportationType,
        VATType,
        CategoryType,
        TransportCostPayer,
        ConfirmationStatus,
        BusinessStatus,
    )
    assert WayBillType.TRANSPORTATION == 2
    assert WayBillStatus.ACTIVE == 1


def test_models_importable():
    from rsge import WayBill, GoodsItem, WayBillSaveResult, CustomsDeclaration
    assert WayBill
    assert GoodsItem
    assert WayBillSaveResult
    assert CustomsDeclaration


def test_exceptions_importable():
    from rsge import (
        RSGeError,
        RSGeAuthenticationError,
        RSGeValidationError,
        RSGeAPIError,
        RSGeConnectionError,
    )
    assert issubclass(RSGeAuthenticationError, RSGeError)
    assert issubclass(RSGeValidationError, RSGeError)
    assert issubclass(RSGeAPIError, RSGeError)
    assert issubclass(RSGeConnectionError, RSGeError)
