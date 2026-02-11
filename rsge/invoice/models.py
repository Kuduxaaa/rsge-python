"""Data models for the RS.ge eAPI Invoice/Declaration service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvoiceAuthResponse:
    """Authentication response from the eAPI.

    Attributes:
        access_token: Bearer token for subsequent requests.
        pin_token: Token for two-factor PIN verification (empty if one-factor).
        masked_mobile: Masked phone number for PIN delivery.
        expires_in: Token expiry time in seconds.
        status_id: Response status ID (0 = success).
        status_text: Response status message.
    """

    access_token: str = ''
    pin_token: str = ''
    masked_mobile: str = ''
    expires_in: int = 0
    status_id: int = 0
    status_text: str = ''

    @property
    def needs_pin(self) -> bool:
        """Whether two-factor PIN verification is required."""
        return bool(self.pin_token) and not self.access_token

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvoiceAuthResponse:
        """Parse from the eAPI JSON response."""
        status = data.get('STATUS', {})
        token_data = data.get('DATA', {})
        return cls(
            access_token  = token_data.get('ACCESS_TOKEN', ''),
            pin_token     = token_data.get('PIN_TOKEN', ''),
            masked_mobile = token_data.get('MASKED_MOBILE', ''),
            expires_in    = int(token_data.get('EXPIRES_IN', 0) or 0),
            status_id     = int(status.get('ID', 0) or 0),
            status_text   = str(status.get('TEXT', '')),
        )


@dataclass
class InvoiceGoods:
    """A single goods/service line item on an invoice.

    Attributes:
        id: Goods line item ID (0 for new items).
        invoice_id: Parent invoice ID (0 for new items).
        goods_name: Product / service description.
        barcode: Barcode value.
        unit_id: Measurement unit ID.
        unit_txt: Measurement unit text (when unit_id=99 'other').
        quantity: Quantity.
        quantity_ext: Additional quantity.
        quantity_stock: Distribution sub-document stock quantity (OUT).
        unit_price: Unit price.
        amount: Total amount (quantity * unit_price).
        vat_amount: VAT amount (OUT).
        vat_type: VAT type (0=standard, 1=zero, 2=exempt).
        vat_type_txt: VAT type text (OUT).
        excise_amount: Excise tax amount.
        excise_id: Excise code ID.
        excise_unit_price: Excise unit price.
        inv_type: Invoice type (OUT).
        inv_category: Invoice category (OUT).
        raw_data: Original dict for unmapped fields.
    """

    id: int = 0
    invoice_id: int = 0
    goods_name: str = ''
    barcode: str = ''
    unit_id: int = 0
    unit_txt: str = ''
    quantity: float = 0
    quantity_ext: str = ''
    quantity_stock: float = 0
    unit_price: float = 0
    amount: float = 0
    vat_amount: float = 0
    vat_type: int = 0
    vat_type_txt: str = ''
    excise_amount: float = 0
    excise_id: int = 0
    excise_unit_price: float = 0
    inv_type: int = 0
    inv_category: int = 0
    raw_data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to eAPI JSON format (writable fields only)."""
        return {
            'ID':               self.id,
            'INVOICE_ID':       self.invoice_id,
            'GOODS_NAME':       self.goods_name,
            'BARCODE':          self.barcode,
            'UNIT_ID':          self.unit_id,
            'UNIT_TXT':         self.unit_txt,
            'QUANTITY':         self.quantity,
            'QUANTITY_EXT':     self.quantity_ext,
            'UNIT_PRICE':       self.unit_price,
            'AMOUNT':           self.amount,
            'VAT_AMOUNT':       self.vat_amount,
            'EXCISE_AMOUNT':    self.excise_amount,
            'EXCISE_ID':        self.excise_id,
            'VAT_TYPE':         self.vat_type,
            'EXCISE_UNIT_PRICE': self.excise_unit_price,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvoiceGoods:
        """Parse from eAPI JSON."""
        return cls(
            id              = int(data.get('ID', 0) or 0),
            invoice_id      = int(data.get('INVOICE_ID', 0) or 0),
            goods_name      = str(data.get('GOODS_NAME', '')),
            barcode         = str(data.get('BARCODE', '')),
            unit_id         = int(data.get('UNIT_ID', 0) or 0),
            unit_txt        = str(data.get('UNIT_TXT', '')),
            quantity        = float(data.get('QUANTITY', 0) or 0),
            quantity_ext    = str(data.get('QUANTITY_EXT', '') or ''),
            quantity_stock  = float(data.get('QUANTITY_STOCK', 0) or 0),
            unit_price      = float(data.get('UNIT_PRICE', 0) or 0),
            amount          = float(data.get('AMOUNT', 0) or 0),
            vat_amount      = float(data.get('VAT_AMOUNT', 0) or 0),
            vat_type        = int(data.get('VAT_TYPE', 0) or 0),
            vat_type_txt    = str(data.get('VAT_TYPE_TXT', '') or ''),
            excise_amount   = float(data.get('EXCISE_AMOUNT', 0) or 0),
            excise_id       = int(data.get('EXCISE_ID', 0) or 0),
            excise_unit_price = float(data.get('EXCISE_UNIT_PRICE', 0) or 0),
            inv_type        = int(data.get('INV_TYPE', 0) or 0),
            inv_category    = int(data.get('INV_CATEGORY', 0) or 0),
            raw_data        = data,
        )


@dataclass
class InvoiceReturn:
    """Return reference on an invoice.

    Attributes:
        return_invoice_id: ID of the invoice being returned.
        corrected_invoice_id: ID of the corrected invoice (OUT).
        inv_number: Invoice number (OUT).
        inv_serie: Invoice serie (OUT).
        buyer: Buyer info (OUT).
        operation_date: Operation date (OUT).
        raw_data: Original dict for unmapped fields.
    """

    return_invoice_id: int = 0
    corrected_invoice_id: int = 0
    inv_number: str = ''
    inv_serie: str = ''
    buyer: str = ''
    operation_date: str = ''
    raw_data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to eAPI JSON format."""
        return {'RETURN_INVOICE_ID': self.return_invoice_id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvoiceReturn:
        """Parse from eAPI JSON."""
        return cls(
            return_invoice_id    = int(data.get('RETURN_INVOICE_ID', 0) or 0),
            corrected_invoice_id = int(data.get('CORRECTED_INVOICE_ID', 0) or 0),
            inv_number           = str(data.get('INV_NUMBER', '')),
            inv_serie            = str(data.get('INV_SERIE', '')),
            buyer                = str(data.get('BUYER', '')),
            operation_date       = str(data.get('OPERATION_DATE', '')),
            raw_data             = data,
        )


@dataclass
class InvoiceAdvance:
    """Advance payment reference on an invoice.

    Attributes:
        parent_invoice_id: Parent invoice ID.
        id: Sub-document ID (distribution or advance).
        operation_date: Operation date (OUT).
        amount: Advance amount.
        inv_number: Invoice number (OUT).
        inv_serie: Invoice serie (OUT).
        buyer: Buyer info (OUT).
        seller: Seller info (OUT).
        inv_category: Invoice category (OUT).
        inv_type: Invoice type (OUT).
        amount_full: Full amount (OUT).
        amount_max: Max amount (OUT).
        activate_date: Activation date (OUT).
        raw_data: Original dict for unmapped fields.
    """

    parent_invoice_id: int = 0
    id: int = 0
    operation_date: str = ''
    amount: float = 0
    inv_number: str = ''
    inv_serie: str = ''
    buyer: str = ''
    seller: str = ''
    inv_category: int = 0
    inv_type: int = 0
    amount_full: float = 0
    amount_max: float = 0
    activate_date: str = ''
    raw_data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to eAPI JSON format."""
        result: dict[str, Any] = {
            'ID': self.id,
            'AMOUNT': self.amount,
        }
        if self.operation_date:
            result['OPERATION_DATE'] = self.operation_date
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvoiceAdvance:
        """Parse from eAPI JSON."""
        return cls(
            parent_invoice_id = int(data.get('PARENT_INVOICE_ID', 0) or 0),
            id                = int(data.get('ID', 0) or 0),
            operation_date    = str(data.get('OPERATION_DATE', '') or ''),
            amount            = float(data.get('AMOUNT', 0) or 0),
            inv_number        = str(data.get('INV_NUMBER', '') or ''),
            inv_serie         = str(data.get('INV_SERIE', '') or ''),
            buyer             = str(data.get('BUYER', '') or ''),
            seller            = str(data.get('SELLER', '') or ''),
            inv_category      = int(data.get('INV_CATEGORY', 0) or 0),
            inv_type          = int(data.get('INV_TYPE', 0) or 0),
            amount_full       = float(data.get('AMOUNT_FULL', 0) or 0),
            amount_max        = float(data.get('AMOUNT_MAX', 0) or 0),
            activate_date     = str(data.get('ACTIVATE_DATE', '') or ''),
            raw_data          = data,
        )


@dataclass
class SubInvoiceDistribution:
    """Distribution sub-invoice reference (OUT parameter).

    Attributes:
        parent_invoice_id: Parent invoice ID.
        sub_invoice_id: Sub-invoice ID.
        inv_number: Invoice number.
        inv_serie: Invoice serie.
        buyer: Buyer info.
        seller: Seller info.
        inv_category: Invoice category.
        inv_type: Invoice type.
        amount_full: Full amount.
        goods_amount_sum: Goods total amount.
        goods_sum: Goods total quantity.
        amount_max: Max amount.
        activate_date: Activation date.
        operation_date: Operation date.
        raw_data: Original dict for unmapped fields.
    """

    parent_invoice_id: int = 0
    sub_invoice_id: int = 0
    inv_number: str = ''
    inv_serie: str = ''
    buyer: str = ''
    seller: str = ''
    inv_category: int = 0
    inv_type: int = 0
    amount_full: float = 0
    goods_amount_sum: float = 0
    goods_sum: float = 0
    amount_max: float = 0
    activate_date: str = ''
    operation_date: str = ''
    raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SubInvoiceDistribution:
        """Parse from eAPI JSON."""
        return cls(
            parent_invoice_id = int(data.get('PARENT_INVOICE_ID', 0) or 0),
            sub_invoice_id    = int(data.get('SUB_INVOICE_ID', 0) or 0),
            inv_number        = str(data.get('INV_NUMBER', '') or ''),
            inv_serie         = str(data.get('INV_SERIE', '') or ''),
            buyer             = str(data.get('BUYER', '') or ''),
            seller            = str(data.get('SELLER', '') or ''),
            inv_category      = int(data.get('INV_CATEGORY', 0) or 0),
            inv_type          = int(data.get('INV_TYPE', 0) or 0),
            amount_full       = float(data.get('AMOUNT_FULL', 0) or 0),
            goods_amount_sum  = float(data.get('GOODS_AMOUNT_SUM', 0) or 0),
            goods_sum         = float(data.get('GOODS_SUM', 0) or 0),
            amount_max        = float(data.get('AMOUNT_MAX', 0) or 0),
            activate_date     = str(data.get('ACTIVATE_DATE', '') or ''),
            operation_date    = str(data.get('OPERATION_DATE', '') or ''),
            raw_data          = data,
        )


@dataclass
class Invoice:
    """Main invoice/declaration document model.

    Attributes:
        id: Invoice ID (0 for new invoices).
        inv_serie: Invoice serie.
        inv_number: Invoice number (OUT, assigned on activation).
        inv_category: Invoice category code.
        inv_type: Invoice type code.
        seller_action: Seller action code (OUT).
        buyer_action: Buyer action code (OUT).
        operation_date: Operation date.
        activate_date: Activation date (OUT).
        create_date: Creation date (OUT).
        confirm_date: Confirmation date (OUT).
        refuse_date: Refusal date (OUT).
        request_cancel_date: Cancel request date (OUT).
        delivery_date: Delivery date (OUT).
        agree_cancel_date: Cancel agreement date (OUT).
        correct_date: Correction date (OUT).
        trans_start_date: Transportation start date.
        correct_reason_id: Correction reason ID.
        tin_seller: Seller TIN.
        tin_buyer: Buyer TIN.
        foreign_buyer: Whether buyer is foreign (0=False, 1=True).
        name_seller: Seller name (OUT).
        name_buyer: Buyer name (OUT).
        seqnum_seller: Seller declaration sequence ID (OUT).
        seqnum_buyer: Buyer declaration sequence ID (OUT).
        seller_status: Seller VAT status (OUT).
        buyer_status: Buyer VAT status (OUT).
        status_txt_geo: Status text in Georgian (OUT).
        status_txt_eng: Status text in English (OUT).
        amount_full: Total amount.
        amount_excise: Total excise amount.
        amount_vat: Total VAT amount.
        amount_max: Max advance amount (OUT).
        trans_start_address: Transport start address.
        trans_end_address: Transport end address.
        trans_start_address_no: Transport start registration number.
        trans_end_address_no: Transport end registration number.
        trans_type: Transport type code.
        trans_type_txt: Transport type text.
        trans_company_tin: Transport company TIN.
        trans_company_name: Transport company name (OUT).
        trans_driver_tin: Driver TIN.
        trans_driver_foreign: Whether driver is foreign.
        trans_driver_name: Driver name (OUT).
        trans_driver_country: Driver country code.
        trans_car_model: Vehicle model.
        trans_car_no: Vehicle plate number.
        trans_trailer_no: Trailer number.
        trans_cost: Transportation cost.
        trans_cost_payer: Cost payer (1=buyer, 2=seller).
        inv_comment: Comment text.
        parent_id: Parent invoice ID (for distribution).
        prev_correction_id: Previous correction invoice ID.
        next_correction_id: Next correction invoice ID (OUT).
        template_name: Template name.
        user_role: User role (OUT: 1=seller, 2=buyer, 3=transporter).
        invoice_goods: List of goods line items.
        invoice_parent_goods: Parent goods for distribution (OUT).
        invoice_return: Return references.
        sub_invoices_distribution: Distribution sub-invoices (OUT).
        invoice_advance: Advance payment references.
        invoice_oil_docs: Oil/petroleum documents.
        raw_data: Original dict for unmapped fields.
    """

    id: int = 0
    inv_serie: str = ''
    inv_number: str = ''
    inv_category: int = 0
    inv_type: int = 0
    seller_action: int = 0
    buyer_action: int = 0
    operation_date: str = ''
    activate_date: str = ''
    create_date: str = ''
    confirm_date: str = ''
    refuse_date: str = ''
    request_cancel_date: str = ''
    delivery_date: str = ''
    agree_cancel_date: str = ''
    correct_date: str = ''
    trans_start_date: str = ''
    correct_reason_id: int = 0
    tin_seller: str = ''
    tin_buyer: str = ''
    foreign_buyer: str = 'false'
    name_seller: str = ''
    name_buyer: str = ''
    seqnum_seller: int | None = None
    seqnum_buyer: int | None = None
    seller_status: int = 0
    buyer_status: int = 0
    status_txt_geo: str = ''
    status_txt_eng: str = ''
    amount_full: float = 0
    amount_excise: float = 0
    amount_vat: float = 0
    amount_max: float = 0
    trans_start_address: str = ''
    trans_end_address: str = ''
    trans_start_address_no: str = ''
    trans_end_address_no: str = ''
    trans_type: int = 0
    trans_type_txt: str = ''
    trans_company_tin: str = ''
    trans_company_name: str = ''
    trans_driver_tin: str = ''
    trans_driver_foreign: str = 'false'
    trans_driver_name: str = ''
    trans_driver_country: str = ''
    trans_car_model: str = ''
    trans_car_no: str = ''
    trans_trailer_no: str = ''
    trans_cost: str = ''
    trans_cost_payer: int = 0
    inv_comment: str = ''
    parent_id: int | None = None
    prev_correction_id: int = 0
    next_correction_id: int | None = None
    template_name: str = ''
    user_role: int = 0
    invoice_goods: list[InvoiceGoods] = field(default_factory=list)
    invoice_parent_goods: list[InvoiceGoods] = field(default_factory=list)
    invoice_return: list[InvoiceReturn] = field(default_factory=list)
    sub_invoices_distribution: list[SubInvoiceDistribution] = field(default_factory=list)
    invoice_advance: list[InvoiceAdvance] = field(default_factory=list)
    invoice_oil_docs: list[dict[str, Any]] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)

    def add_goods(
        self,
        goods_name: str,
        quantity: float,
        unit_price: float,
        unit_id: int = 1,
        unit_txt: str = '',
        barcode: str = '',
        vat_type: int = 0,
        excise_id: int = 0,
        excise_amount: float = 0,
        excise_unit_price: float = 0,
    ) -> InvoiceGoods:
        """Add a goods line item with auto-calculated amount.

        Args:
            goods_name: Product / service name.
            quantity: Quantity.
            unit_price: Price per unit.
            unit_id: Measurement unit ID (default 1).
            unit_txt: Unit text (used when unit_id=99).
            barcode: Barcode value.
            vat_type: VAT type (0=standard, 1=zero, 2=exempt).
            excise_id: Excise code ID.
            excise_amount: Excise amount.
            excise_unit_price: Excise unit price.

        Returns:
            The created InvoiceGoods item.
        """
        item = InvoiceGoods(
            goods_name=goods_name,
            quantity=quantity,
            unit_price=unit_price,
            amount=quantity * unit_price,
            unit_id=unit_id,
            unit_txt=unit_txt,
            barcode=barcode,
            vat_type=vat_type,
            excise_id=excise_id,
            excise_amount=excise_amount,
            excise_unit_price=excise_unit_price,
        )
        self.invoice_goods.append(item)
        return item

    def to_dict(self) -> dict[str, Any]:
        """Serialize to eAPI JSON format (writable fields only)."""
        result: dict[str, Any] = {
            'ID':                     self.id,
            'INV_SERIE':              self.inv_serie,
            'INV_NUMBER':             self.inv_number,
            'INV_CATEGORY':           self.inv_category,
            'INV_TYPE':               self.inv_type,
            'SELLER_ACTION':          self.seller_action,
            'BUYER_ACTION':           self.buyer_action,
            'OPERATION_DATE':         self.operation_date,
            'TRANS_START_DATE':       self.trans_start_date,
            'CORRECT_REASON_ID':      self.correct_reason_id,
            'TIN_SELLER':             self.tin_seller,
            'TIN_BUYER':              self.tin_buyer,
            'FOREIGN_BUYER':          self.foreign_buyer,
            'AMOUNT_FULL':            self.amount_full,
            'AMOUNT_EXCISE':          self.amount_excise,
            'AMOUNT_VAT':             self.amount_vat,
            'TRANS_START_ADDRESS':    self.trans_start_address,
            'TRANS_END_ADDRESS':      self.trans_end_address,
            'TRANS_START_ADDRESS_NO': self.trans_start_address_no,
            'TRANS_END_ADDRESS_NO':   self.trans_end_address_no,
            'TRANS_TYPE':             self.trans_type,
            'TRANS_TYPE_TXT':         self.trans_type_txt,
            'TRANS_COMPANY_TIN':      self.trans_company_tin,
            'TRANS_DRIVER_TIN':       self.trans_driver_tin,
            'TRANS_DRIVER_FOREIGN':   self.trans_driver_foreign,
            'TRANS_DRIVER_COUNTRY':   self.trans_driver_country,
            'TRANS_CAR_MODEL':        self.trans_car_model,
            'TRANS_CAR_NO':           self.trans_car_no,
            'TRANS_TRAILER_NO':       self.trans_trailer_no,
            'TRANS_COST':             self.trans_cost,
            'TRANS_COST_PAYER':       self.trans_cost_payer,
            'INV_COMMENT':            self.inv_comment,
            'PREV_CORRECTION_ID':     self.prev_correction_id,
            'TEMPLATE_NAME':          self.template_name,
            'INVOICE_GOODS':          [g.to_dict() for g in self.invoice_goods],
            'INVOICE_PARENT_GOODS':   [],
            'INVOICE_RETURN':         [r.to_dict() for r in self.invoice_return],
            'SUB_INVOICES_DISTRIBUTION': [],
            'INVOICE_ADVANCE':        [a.to_dict() for a in self.invoice_advance],
            'INVOICE_OIL_DOCS':       self.invoice_oil_docs,
        }
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Invoice:
        """Parse from eAPI JSON (INVOICE object)."""
        goods = [InvoiceGoods.from_dict(g) for g in data.get('INVOICE_GOODS', []) or []]
        parent_goods = [
            InvoiceGoods.from_dict(g) for g in data.get('INVOICE_PARENT_GOODS', []) or []
        ]
        returns = [InvoiceReturn.from_dict(r) for r in data.get('INVOICE_RETURN', []) or []]
        sub_dist = [
            SubInvoiceDistribution.from_dict(s)
            for s in data.get('SUB_INVOICES_DISTRIBUTION', []) or []
        ]
        advances = [InvoiceAdvance.from_dict(a) for a in data.get('INVOICE_ADVANCE', []) or []]

        return cls(
            id                       = int(data.get('ID', 0) or 0),
            inv_serie                = str(data.get('INV_SERIE', '') or ''),
            inv_number               = str(data.get('INV_NUMBER', '') or ''),
            inv_category             = int(data.get('INV_CATEGORY', 0) or 0),
            inv_type                 = int(data.get('INV_TYPE', 0) or 0),
            seller_action            = int(data.get('SELLER_ACTION', 0) or 0),
            buyer_action             = int(data.get('BUYER_ACTION', 0) or 0),
            operation_date           = str(data.get('OPERATION_DATE', '') or ''),
            activate_date            = str(data.get('ACTIVATE_DATE', '') or ''),
            create_date              = str(data.get('CREATE_DATE', '') or ''),
            confirm_date             = str(data.get('CONFIRM_DATE', '') or ''),
            refuse_date              = str(data.get('REFUSE_DATE', '') or ''),
            request_cancel_date      = str(data.get('REQUEST_CANCEL_DATE', '') or ''),
            delivery_date            = str(data.get('DELIVERY_DATE', '') or ''),
            agree_cancel_date        = str(data.get('AGREE_CANCEL_DATE', '') or ''),
            correct_date             = str(data.get('CORRECT_DATE', '') or ''),
            trans_start_date         = str(data.get('TRANS_START_DATE', '') or ''),
            correct_reason_id        = int(data.get('CORRECT_REASON_ID', 0) or 0),
            tin_seller               = str(data.get('TIN_SELLER', '') or ''),
            tin_buyer                = str(data.get('TIN_BUYER', '') or ''),
            foreign_buyer            = str(data.get('FOREIGN_BUYER', 'false') or 'false'),
            name_seller              = str(data.get('NAME_SELLER', '') or ''),
            name_buyer               = str(data.get('NAME_BUYER', '') or ''),
            seqnum_seller            = data.get('SEQNUM_SELLER'),
            seqnum_buyer             = data.get('SEQNUM_BUYER'),
            seller_status            = int(data.get('SELLER_STATUS', 0) or 0),
            buyer_status             = int(data.get('BUYER_STATUS', 0) or 0),
            status_txt_geo           = str(data.get('STATUS_TXT_GEO', '') or ''),
            status_txt_eng           = str(data.get('STATUS_TXT_ENG', '') or ''),
            amount_full              = float(data.get('AMOUNT_FULL', 0) or 0),
            amount_excise            = float(data.get('AMOUNT_EXCISE', 0) or 0),
            amount_vat               = float(data.get('AMOUNT_VAT', 0) or 0),
            amount_max               = float(data.get('AMOUNT_MAX', 0) or 0),
            trans_start_address      = str(data.get('TRANS_START_ADDRESS', '') or ''),
            trans_end_address        = str(data.get('TRANS_END_ADDRESS', '') or ''),
            trans_start_address_no   = str(data.get('TRANS_START_ADDRESS_NO', '') or ''),
            trans_end_address_no     = str(data.get('TRANS_END_ADDRESS_NO', '') or ''),
            trans_type               = int(data.get('TRANS_TYPE', 0) or 0),
            trans_type_txt           = str(data.get('TRANS_TYPE_TXT', '') or ''),
            trans_company_tin        = str(data.get('TRANS_COMPANY_TIN', '') or ''),
            trans_company_name       = str(data.get('TRANS_COMPANY_NAME', '') or ''),
            trans_driver_tin         = str(data.get('TRANS_DRIVER_TIN', '') or ''),
            trans_driver_foreign     = str(data.get('TRANS_DRIVER_FOREIGN', 'false') or 'false'),
            trans_driver_name        = str(data.get('TRANS_DRIVER_NAME', '') or ''),
            trans_driver_country     = str(data.get('TRANS_DRIVER_COUNTRY', '') or ''),
            trans_car_model          = str(data.get('TRANS_CAR_MODEL', '') or ''),
            trans_car_no             = str(data.get('TRANS_CAR_NO', '') or ''),
            trans_trailer_no         = str(data.get('TRANS_TRAILER_NO', '') or ''),
            trans_cost               = str(data.get('TRANS_COST', '') or ''),
            trans_cost_payer         = int(data.get('TRANS_COST_PAYER', 0) or 0),
            inv_comment              = str(data.get('INV_COMMENT', '') or ''),
            parent_id                = data.get('PARENT_ID'),
            prev_correction_id       = int(data.get('PREV_CORRECTION_ID', 0) or 0),
            next_correction_id       = data.get('NEXT_CORRECTION_ID'),
            template_name            = str(data.get('TEMPLATE_NAME', '') or ''),
            user_role                = int(data.get('USER_ROLE', 0) or 0),
            invoice_goods            = goods,
            invoice_parent_goods     = parent_goods,
            invoice_return           = returns,
            sub_invoices_distribution = sub_dist,
            invoice_advance          = advances,
            invoice_oil_docs         = data.get('INVOICE_OIL_DOCS', []) or [],
            raw_data                 = data,
        )


@dataclass
class InvoiceAction:
    """Invoice status/action entry from GetActions.

    Attributes:
        id: Status ID.
        name: Status name.
        seller_action: Seller action code.
        buyer_action: Buyer action code.
    """

    id: int = 0
    name: str = ''
    seller_action: int = 0
    buyer_action: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvoiceAction:
        """Parse from eAPI JSON."""
        return cls(
            id            = int(data.get('ID', 0) or 0),
            name          = str(data.get('NAME', '')),
            seller_action = int(data.get('SELLER_ACTION', 0) or 0),
            buyer_action  = int(data.get('BUYER_ACTION', 0) or 0),
        )


@dataclass
class Unit:
    """Measurement unit from GetUnits.

    Attributes:
        value: Unit ID.
        label: Unit display label.
    """

    value: str = ''
    label: str = ''

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Unit:
        """Parse from eAPI JSON."""
        return cls(
            value = str(data.get('value', '')),
            label = str(data.get('label', '')),
        )


@dataclass
class OrgInfo:
    """Organization info from GetOrgInfoByTin.

    Attributes:
        tin: Tax identification number.
        address: Registered address.
        is_vat_payer: Whether the org is a VAT payer.
        is_diplomat: Whether the org has diplomatic status.
        name: Organization name.
        raw_data: Original dict for unmapped fields.
    """

    tin: str = ''
    address: str = ''
    is_vat_payer: bool = False
    is_diplomat: bool = False
    name: str = ''
    raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OrgInfo:
        """Parse from eAPI JSON."""
        return cls(
            tin          = str(data.get('Tin', '')),
            address      = str(data.get('Address', '')),
            is_vat_payer = bool(data.get('IsVatPayer', False)),
            is_diplomat  = bool(data.get('IsDiplomat', False)),
            name         = str(data.get('Name', '')),
            raw_data     = data,
        )


@dataclass
class BarCode:
    """Barcode catalog entry.

    Attributes:
        barcode: Barcode value.
        goods_name: Product name.
        unit_id: Unit ID.
        unit_txt: Unit text.
        vat_type: VAT type.
        vat_type_txt: VAT type text.
        unit_price: Unit price.
    """

    barcode: str = ''
    goods_name: str = ''
    unit_id: int = 0
    unit_txt: str = ''
    vat_type: int = 0
    vat_type_txt: str = ''
    unit_price: float = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BarCode:
        """Parse from eAPI JSON."""
        return cls(
            barcode      = str(data.get('BARCODE', '')),
            goods_name   = str(data.get('GOODS_NAME', '')),
            unit_id      = int(data.get('UNIT_ID', 0) or 0),
            unit_txt     = str(data.get('UNIT_TXT', '')),
            vat_type     = int(data.get('VAT_TYPE', 0) or 0),
            vat_type_txt = str(data.get('VAT_TYPE_TXT', '')),
            unit_price   = float(data.get('UNIT_PRICE', 0) or 0),
        )


@dataclass
class TransactionResult:
    """Result from GetTransactionResult (async save).

    Attributes:
        invoice_id: Created/updated invoice ID.
        raw_data: Original dict for unmapped fields.
    """

    invoice_id: int = 0
    raw_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TransactionResult:
        """Parse from eAPI JSON."""
        return cls(
            invoice_id = int(data.get('INVOICE_ID', 0) or 0),
            raw_data   = data,
        )
