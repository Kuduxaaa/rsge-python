"""Data models for the RS.ge Customs Declarations REST API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CustomsAuthResponse:
    """Authentication response from the customs API.

    Attributes:
        access_token: Bearer token for subsequent requests.
        status: Response status code.
        message: Status message.
    """

    access_token: str = ''
    status: int = 0
    message: str = ''

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CustomsAuthResponse:
        """Parse from the API JSON response."""
        status_data = data.get('STATUS', {})
        token_data = data.get('DATA', {})
        return cls(
            access_token = token_data.get('ACCESS_TOKEN', ''),
            status       = status_data.get('CODE', 0),
            message      = status_data.get('MESSAGE', ''),
        )


@dataclass
class CustomsDeclaration:
    """A single customs declaration record.

    Attributes:
        declaration_number: Unique declaration number.
        assessment_date: Date the declaration was assessed.
        commodity_code: HS commodity code.
        description: Goods description.
        quantity: Declared quantity.
        net_weight: Net weight in kg.
        gross_weight: Gross weight in kg.
        statistical_value: Statistical value.
        customs_value: Customs value.
        duty_amount: Customs duty amount.
        vat_amount: VAT amount.
        excise_amount: Excise tax amount.
        country_of_origin: Country of origin code.
        country_of_dispatch: Country of dispatch code.
        raw_data: The original dict for any unmapped fields.
    """

    declaration_number: str = ''
    assessment_date: str = ''
    commodity_code: str = ''
    description: str = ''
    quantity: float = 0
    net_weight: float = 0
    gross_weight: float = 0
    statistical_value: float = 0
    customs_value: float = 0
    duty_amount: float = 0
    vat_amount: float = 0
    excise_amount: float = 0
    country_of_origin: str = ''
    country_of_dispatch: str = ''
    raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CustomsDeclaration:
        """Parse from the API JSON response dict."""
        return cls(
            declaration_number  = str(data.get('DECLARATION_NUMBER', '')),
            assessment_date     = str(data.get('ASSESSMENT_DATE', '')),
            commodity_code      = str(data.get('COMMODITY_CODE', '')),
            description         = str(data.get('DESCRIPTION', '')),
            quantity            = float(data.get('QUANTITY', 0) or 0),
            net_weight          = float(data.get('NET_WEIGHT', 0) or 0),
            gross_weight        = float(data.get('GROSS_WEIGHT', 0) or 0),
            statistical_value   = float(data.get('STATISTICAL_VALUE', 0) or 0),
            customs_value       = float(data.get('CUSTOMS_VALUE', 0) or 0),
            duty_amount         = float(data.get('DUTY_AMOUNT', 0) or 0),
            vat_amount          = float(data.get('VAT_AMOUNT', 0) or 0),
            excise_amount       = float(data.get('EXCISE_AMOUNT', 0) or 0),
            country_of_origin   = str(data.get('COUNTRY_OF_ORIGIN', '')),
            country_of_dispatch = str(data.get('COUNTRY_OF_DISPATCH', '')),
            raw_data            = data,
        )
