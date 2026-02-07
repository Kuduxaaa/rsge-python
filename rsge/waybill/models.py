"""Data models for the RS.ge WayBill service.

All models are plain dataclasses that can be serialized to/from XML
for communication with the SOAP API.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from rsge.core.xml_utils import add_child, build_element, get_decimal, get_int, get_text
from rsge.waybill.enums import (
    CategoryType,
    TransportCostPayer,
    VATType,
    WayBillStatus,
    WayBillType,
)


def _safe_enum(enum_cls: type, value: int) -> Any:
    """Safely convert an integer to an enum member, returning the raw value on failure."""
    try:
        return enum_cls(value)
    except ValueError:
        return value


@dataclass
class ServiceUser:
    """A registered service user account.

    Attributes:
        id: Service user ID.
        user_name: Login username.
        un_id: Taxpayer unique number.
        ip: Whitelisted IP address.
        name: Object / store name.
    """

    id: int
    user_name: str
    un_id: int
    ip: str
    name: str

    @classmethod
    def from_xml(cls, elem: ET.Element) -> ServiceUser:
        """Parse a ServiceUser XML element."""
        return cls(
            id        = get_int(elem, 'ID'),
            user_name = get_text(elem, 'USER_NAME'),
            un_id     = get_int(elem, 'UN_ID'),
            ip        = get_text(elem, 'IP'),
            name      = get_text(elem, 'NAME'),
        )


@dataclass
class AkcizCode:
    """Excise (akciz) commodity code.

    Attributes:
        id: Excise code ID.
        title: Full display title.
        measurement: Unit of measurement.
        commodity_code: Commodity code.
        rate: Excise tax rate.
    """

    id: int
    title: str
    measurement: str
    commodity_code: str
    rate: float

    @classmethod
    def from_xml(cls, elem: ET.Element) -> AkcizCode:
        """Parse an AKCIZ_CODE XML element."""
        return cls(
            id             = get_int(elem, 'ID'),
            title          = get_text(elem, 'TITLE'),
            measurement    = get_text(elem, 'MEASUREMENT'),
            commodity_code = get_text(elem, 'SAKON_KODI'),
            rate           = get_decimal(elem, 'AKCIS_GANAKV'),
        )


@dataclass
class WayBillTypeInfo:
    """Waybill type reference record.

    Attributes:
        id: Type ID.
        name: Type display name.
    """

    id: int
    name: str

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WayBillTypeInfo:
        """Parse a WAYBILL_TYPE XML element."""
        return cls(
            id   = get_int(elem, 'ID'),
            name = get_text(elem, 'NAME'),
        )


@dataclass
class WayBillUnit:
    """Measurement unit reference record.

    Attributes:
        id: Unit ID.
        name: Unit display name.
    """

    id: int
    name: str

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WayBillUnit:
        """Parse a WAYBILL_UNIT XML element."""
        return cls(
            id   = get_int(elem, 'ID'),
            name = get_text(elem, 'NAME'),
        )


@dataclass
class TransportType:
    """Transport type reference record.

    Attributes:
        id: Transport type ID.
        name: Display name.
    """

    id: int
    name: str

    @classmethod
    def from_xml(cls, elem: ET.Element) -> TransportType:
        """Parse a TRANSPORT_TYPE XML element."""
        return cls(
            id   = get_int(elem, 'ID'),
            name = get_text(elem, 'NAME'),
        )


@dataclass
class WoodType:
    """Wood/timber type reference record.

    Attributes:
        id: Wood type ID.
        name: Short name.
        description: Extended description.
    """

    id: int
    name: str
    description: str

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WoodType:
        """Parse a WOOD_TYPES XML element."""
        return cls(
            id          = get_int(elem, 'ID'),
            name        = get_text(elem, 'NAME'),
            description = get_text(elem, 'DESCRIPTION'),
        )


@dataclass
class ErrorCode:
    """API error code reference.

    Attributes:
        id: Numeric error code (negative).
        text: Error description.
        error_type: 1 = waybill, 2 = goods item, 3 = invoice.
    """

    id: int
    text: str
    error_type: int

    @classmethod
    def from_xml(cls, elem: ET.Element) -> ErrorCode:
        """Parse a WAYBILL_TYPE error code element."""
        return cls(
            id         = get_int(elem, 'ID'),
            text       = get_text(elem, 'TEXT'),
            error_type = get_int(elem, 'TYPE'),
        )


@dataclass
class GoodsItem:
    """A single goods/product line item within a waybill.

    Attributes:
        id: Record ID (0 for new items).
        name: Product name (required).
        unit_id: Measurement unit ID (required).
        unit_txt: Unit name (required when unit_id == 99).
        quantity: Quantity (required).
        price: Unit price (required).
        status: 1 = active, -1 = delete this item.
        amount: Total amount (required, typically quantity * price).
        bar_code: Barcode or medicine registration number (required).
        akciz_id: Excise code ID (0 if not excise goods).
        vat_type: VAT taxation type.
        quantity_ext: Auxiliary quantity (optional).
        wood_label: Timber label number (for wood category).
        wood_type_id: Wood type ID (for wood category).
    """

    id: int = 0
    name: str = ''
    unit_id: int = 1
    unit_txt: str = ''
    quantity: float = 0
    price: float = 0
    status: int = 1
    amount: float = 0
    bar_code: str = ''
    akciz_id: int = 0
    vat_type: VATType = VATType.REGULAR
    quantity_ext: float = 0
    wood_label: str = ''
    wood_type_id: int = 0

    def to_xml(self) -> ET.Element:
        """Serialize this goods item to an XML GOODS element."""
        goods = build_element('GOODS')
        add_child(goods, 'ID', self.id)
        add_child(goods, 'W_NAME', self.name)
        add_child(goods, 'UNIT_ID', self.unit_id)
        add_child(goods, 'UNIT_TXT', self.unit_txt)
        add_child(goods, 'QUANTITY', self.quantity)
        add_child(goods, 'PRICE', self.price)
        add_child(goods, 'STATUS', self.status)
        add_child(goods, 'AMOUNT', self.amount)
        add_child(goods, 'BAR_CODE', self.bar_code)
        add_child(goods, 'A_ID', self.akciz_id)
        add_child(goods, 'VAT_TYPE', int(self.vat_type))
        add_child(goods, 'QUANTITY_EXT', self.quantity_ext)
        add_child(goods, 'WOOD_LABEL', self.wood_label)
        add_child(goods, 'W_ID', self.wood_type_id)
        return goods

    @classmethod
    def from_xml(cls, elem: ET.Element) -> GoodsItem:
        """Parse a GOODS XML element."""
        return cls(
            id           = get_int(elem, 'ID'),
            name         = get_text(elem, 'W_NAME'),
            unit_id      = get_int(elem, 'UNIT_ID'),
            unit_txt     = get_text(elem, 'UNIT_TXT'),
            quantity     = get_decimal(elem, 'QUANTITY'),
            price        = get_decimal(elem, 'PRICE'),
            status       = get_int(elem, 'STATUS', 1),
            amount       = get_decimal(elem, 'AMOUNT'),
            bar_code     = get_text(elem, 'BAR_CODE'),
            akciz_id     = get_int(elem, 'A_ID'),
            vat_type     = VATType(get_int(elem, 'VAT_TYPE')),
            quantity_ext = get_decimal(elem, 'QUANTITY_EXT'),
            wood_label   = get_text(elem, 'WOOD_LABEL'),
            wood_type_id = get_int(elem, 'W_ID'),
        )


@dataclass
class WoodDocument:
    """A wood-origin document attached to a timber waybill.

    Attributes:
        id: Record ID (0 for new).
        doc_number: Document number.
        doc_date: Document issue date.
        doc_description: Document type/description.
        status: 1 = active, -1 = delete.
    """

    id: int = 0
    doc_number: str = ''
    doc_date: datetime | None = None
    doc_description: str = ''
    status: int = 1

    def to_xml(self) -> ET.Element:
        """Serialize to a WOODDOCUMENT XML element."""
        doc = build_element('WOODDOCUMENT')
        add_child(doc, 'ID', self.id)
        add_child(doc, 'DOC_N', self.doc_number)
        if self.doc_date:
            add_child(doc, 'DOC_DATE', self.doc_date.strftime('%Y-%m-%dT%H:%M:%S'))
        add_child(doc, 'DOC_DESC', self.doc_description)
        add_child(doc, 'STATUS', self.status)
        return doc

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WoodDocument:
        """Parse a WOODDOCUMENT XML element."""
        date_str = get_text(elem, 'DOC_DATE')
        doc_date = None
        if date_str:
            try:
                doc_date = datetime.fromisoformat(date_str)
            except ValueError:
                pass

        return cls(
            id              = get_int(elem, 'ID'),
            doc_number      = get_text(elem, 'DOC_N'),
            doc_date        = doc_date,
            doc_description = get_text(elem, 'DOC_DESC'),
            status          = get_int(elem, 'STATUS', 1),
        )


@dataclass
class SubWayBill:
    """Reference to a sub-waybill under a distribution waybill.

    Attributes:
        id: Sub-waybill ID.
        waybill_number: Sub-waybill number.
    """

    id: int = 0
    waybill_number: str = ''

    @classmethod
    def from_xml(cls, elem: ET.Element) -> SubWayBill:
        """Parse a SUB_WAYBILL XML element."""
        return cls(
            id             = get_int(elem, 'ID'),
            waybill_number = get_text(elem, 'WAYBILL_NUMBER'),
        )


@dataclass
class WayBill:
    """Complete electronic commodity waybill.

    Attributes:
        id: Waybill ID (0 for new waybills).
        waybill_type: Type of waybill.
        buyer_tin: Buyer's personal/identification number.
        check_buyer_tin: 1 if Georgian citizen, 0 if foreign.
        buyer_name: Buyer's name.
        start_address: Transportation start address.
        end_address: Transportation end address.
        driver_tin: Driver's personal number.
        check_driver_tin: 1 if Georgian citizen, 0 if foreign.
        driver_name: Driver's name.
        transport_cost: Transportation cost.
        reception_info: Supplier/sender information.
        receiver_info: Receiver information.
        delivery_date: Delivery date (fill before closing).
        status: Current waybill status.
        seller_un_id: Seller's unique number.
        parent_id: Parent waybill ID (for sub-waybills).
        full_amount: Total waybill amount.
        car_number: Vehicle registration number.
        waybill_number: Assigned waybill number.
        s_user_id: Service user ID.
        begin_date: Transportation start date.
        transport_cost_payer: Who pays transport cost.
        transport_type_id: Transport type ID.
        transport_type_txt: Transport type text (when type is other).
        comment: Freeform comment.
        category: Waybill category (regular or wood).
        is_medicine: 1 if medicine waybill.
        wood_labels: Timber label numbers.
        transporter_tin: Transporter company TIN (for forwarded waybills).
        goods_list: List of goods/product items.
        wood_docs_list: List of wood-origin documents.
        sub_waybills: List of sub-waybill references.
        create_date: Creation date (read-only, set by server).
        activate_date: Activation date (read-only).
        close_date: Closing date (read-only).
        customs_status: Customs confirmation status.
        customs_name: Customs checkpoint name.
    """

    id: int = 0
    waybill_type: WayBillType | int = WayBillType.TRANSPORTATION
    buyer_tin: str = ''
    check_buyer_tin: int = 1
    buyer_name: str = ''
    start_address: str = ''
    end_address: str = ''
    driver_tin: str = ''
    check_driver_tin: int = 1
    driver_name: str = ''
    transport_cost: float = 0
    reception_info: str = ''
    receiver_info: str = ''
    delivery_date: str = ''
    status: WayBillStatus | int = WayBillStatus.SAVED
    seller_un_id: int = 0
    parent_id: str = ''
    full_amount: float = 0
    car_number: str = ''
    waybill_number: str = ''
    s_user_id: int = 0
    begin_date: str = ''
    transport_cost_payer: TransportCostPayer | int = TransportCostPayer.SELLER
    transport_type_id: int = 1
    transport_type_txt: str = ''
    comment: str = ''
    category: CategoryType | int = CategoryType.REGULAR
    is_medicine: int = 0
    wood_labels: str = ''
    transporter_tin: str = ''
    goods_list: list[GoodsItem] = field(default_factory=list)
    wood_docs_list: list[WoodDocument] = field(default_factory=list)
    sub_waybills: list[SubWayBill] = field(default_factory=list)
    create_date: str = ''
    activate_date: str = ''
    close_date: str = ''
    customs_status: str = ''
    customs_name: str = ''

    def add_goods(
        self,
        name: str,
        unit_id: int,
        quantity: float,
        price: float,
        bar_code: str,
        *,
        unit_txt: str = '',
        akciz_id: int = 0,
        vat_type: VATType = VATType.REGULAR,
        quantity_ext: float = 0,
    ) -> GoodsItem:
        """Add a goods item to this waybill.

        Args:
            name: Product name.
            unit_id: Measurement unit ID.
            quantity: Quantity.
            price: Unit price.
            bar_code: Barcode or medicine registration number.
            unit_txt: Unit text (required if unit_id == 99).
            akciz_id: Excise code ID (0 if not applicable).
            vat_type: VAT type.
            quantity_ext: Auxiliary quantity.

        Returns:
            The newly created GoodsItem.
        """
        item = GoodsItem(
            name         = name,
            unit_id      = unit_id,
            quantity     = quantity,
            price        = price,
            amount       = round(quantity * price, 2),
            bar_code     = bar_code,
            unit_txt     = unit_txt,
            akciz_id     = akciz_id,
            vat_type     = vat_type,
            quantity_ext = quantity_ext,
        )

        self.goods_list.append(item)
        self._recalculate_total()
        return item

    def add_wood_document(
        self,
        doc_number: str,
        doc_date: datetime,
        doc_description: str,
    ) -> WoodDocument:
        """Add a wood-origin document to this waybill.

        Args:
            doc_number: Document number.
            doc_date: Document issue date.
            doc_description: Document type description.

        Returns:
            The newly created WoodDocument.
        """
        doc = WoodDocument(
            doc_number      = doc_number,
            doc_date        = doc_date,
            doc_description = doc_description,
        )

        self.wood_docs_list.append(doc)
        return doc

    def _recalculate_total(self) -> None:
        """Recalculate full_amount from goods list."""
        self.full_amount = round(
            sum(g.amount for g in self.goods_list if g.status == 1), 2
        )

    def to_xml(self) -> ET.Element:
        """Serialize this waybill to the XML format expected by save_waybill.

        Returns:
            An ET.Element representing the WAYBILL structure.
        """
        wb = build_element('WAYBILL')

        sub_wb_elem = add_child(wb, 'SUB_WAYBILLS')
        for sub in self.sub_waybills:
            sub_elem = add_child(sub_wb_elem, 'SUB_WAYBILL')
            add_child(sub_elem, 'ID', sub.id)
            add_child(sub_elem, 'WAYBILL_NUMBER', sub.waybill_number)

        goods_elem = add_child(wb, 'GOODS_LIST')
        for item in self.goods_list:
            goods_elem.append(item.to_xml())

        wood_docs_elem = add_child(wb, 'WOOD_DOCS_LIST')
        for doc in self.wood_docs_list:
            wood_docs_elem.append(doc.to_xml())

        add_child(wb, 'ID', self.id)
        add_child(wb, 'TYPE', int(self.waybill_type))
        add_child(wb, 'BUYER_TIN', self.buyer_tin)
        add_child(wb, 'CHEK_BUYER_TIN', self.check_buyer_tin)
        add_child(wb, 'BUYER_NAME', self.buyer_name)
        add_child(wb, 'START_ADDRESS', self.start_address)
        add_child(wb, 'END_ADDRESS', self.end_address)
        add_child(wb, 'DRIVER_TIN', self.driver_tin)
        add_child(wb, 'CHEK_DRIVER_TIN', self.check_driver_tin)
        add_child(wb, 'DRIVER_NAME', self.driver_name)
        add_child(wb, 'TRANSPORT_COAST', self.transport_cost)
        add_child(wb, 'RECEPTION_INFO', self.reception_info)
        add_child(wb, 'RECEIVER_INFO', self.receiver_info)
        add_child(wb, 'DELIVERY_DATE', self.delivery_date)
        add_child(wb, 'STATUS', int(self.status))
        add_child(wb, 'SELER_UN_ID', self.seller_un_id)
        add_child(wb, 'PAR_ID', self.parent_id)
        add_child(wb, 'FULL_AMOUNT', self.full_amount)
        add_child(wb, 'CAR_NUMBER', self.car_number)
        add_child(wb, 'WAYBILL_NUMBER', self.waybill_number)
        add_child(wb, 'S_USER_ID', self.s_user_id)
        add_child(wb, 'BEGIN_DATE', self.begin_date)
        add_child(wb, 'TRAN_COST_PAYER', int(self.transport_cost_payer))
        add_child(wb, 'TRANS_ID', self.transport_type_id)
        add_child(wb, 'TRANS_TXT', self.transport_type_txt)
        add_child(wb, 'COMMENT', self.comment)
        add_child(wb, 'CATEGORY', int(self.category))
        add_child(wb, 'IS_MED', self.is_medicine)
        add_child(wb, 'WOOD_LABELS', self.wood_labels)

        if self.transporter_tin:
            add_child(wb, 'TRANSPORTER_TIN', self.transporter_tin)

        return wb

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WayBill:
        """Parse a WAYBILL XML response element into a WayBill object.

        Args:
            elem: The XML element to parse.

        Returns:
            A fully populated WayBill instance.
        """
        goods_elem = elem.find('GOODS_LIST')
        goods_list = (
            [GoodsItem.from_xml(g) for g in goods_elem.findall('GOODS')]
            if goods_elem is not None else []
        )

        wood_elem = elem.find('WOOD_DOCS_LIST')
        wood_docs = (
            [WoodDocument.from_xml(d) for d in wood_elem.findall('WOODDOCUMENT')]
            if wood_elem is not None else []
        )

        sub_elem = elem.find('SUB_WAYBILLS')
        sub_waybills = (
            [SubWayBill.from_xml(s) for s in sub_elem.findall('SUB_WAYBILL')]
            if sub_elem is not None else []
        )

        return cls(
            id                   = get_int(elem, 'ID'),
            waybill_type         = _safe_enum(WayBillType, get_int(elem, 'TYPE')),
            buyer_tin            = get_text(elem, 'BUYER_TIN'),
            check_buyer_tin      = get_int(elem, 'CHEK_BUYER_TIN'),
            buyer_name           = get_text(elem, 'BUYER_NAME'),
            start_address        = get_text(elem, 'START_ADDRESS'),
            end_address          = get_text(elem, 'END_ADDRESS'),
            driver_tin           = get_text(elem, 'DRIVER_TIN'),
            check_driver_tin     = get_int(elem, 'CHEK_DRIVER_TIN'),
            driver_name          = get_text(elem, 'DRIVER_NAME'),
            transport_cost       = get_decimal(elem, 'TRANSPORT_COAST'),
            reception_info       = get_text(elem, 'RECEPTION_INFO'),
            receiver_info        = get_text(elem, 'RECEIVER_INFO'),
            delivery_date        = get_text(elem, 'DELIVERY_DATE'),
            status               = _safe_enum(WayBillStatus, get_int(elem, 'STATUS')),
            seller_un_id         = get_int(elem, 'SELER_UN_ID'),
            parent_id            = get_text(elem, 'PAR_ID'),
            full_amount          = get_decimal(elem, 'FULL_AMOUNT'),
            car_number           = get_text(elem, 'CAR_NUMBER'),
            waybill_number       = get_text(elem, 'WAYBILL_NUMBER'),
            s_user_id            = get_int(elem, 'S_USER_ID'),
            begin_date           = get_text(elem, 'BEGIN_DATE'),
            transport_cost_payer = _safe_enum(
                TransportCostPayer, get_int(elem, 'TRAN_COST_PAYER', 2),
            ),
            transport_type_id    = get_int(elem, 'TRANS_ID'),
            transport_type_txt   = get_text(elem, 'TRANS_TXT'),
            comment              = get_text(elem, 'COMMENT'),
            category             = _safe_enum(CategoryType, get_int(elem, 'CATEGORY')),
            is_medicine          = get_int(elem, 'IS_MED'),
            wood_labels          = get_text(elem, 'WOOD_LABELS'),
            goods_list           = goods_list,
            wood_docs_list       = wood_docs,
            sub_waybills         = sub_waybills,
            create_date          = get_text(elem, 'CREATE_DATE'),
            activate_date        = get_text(elem, 'ACTIVATE_DATE'),
            close_date           = get_text(elem, 'CLOSE_DATE'),
            customs_status       = get_text(elem, 'CUST_STATUS'),
            customs_name         = get_text(elem, 'CUST_NAME'),
        )


@dataclass
class WayBillSaveResult:
    """Result returned by WayBillClient.save_waybill.

    Attributes:
        status: 0 on success, negative on error.
        waybill_id: The saved waybill's ID (if successful).
        goods_results: List of goods items with their assigned IDs or error codes.
    """

    status: int
    waybill_id: int
    goods_results: list[dict[str, Any]] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        """Whether the save operation succeeded."""
        return self.status == 0

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WayBillSaveResult:
        """Parse a RESULT XML element."""
        goods_results: list[dict[str, Any]] = []
        goods_list = elem.find('GOODS_LIST')
        if goods_list is not None:
            for g in goods_list.findall('GOODS'):
                goods_results.append({
                    'id':     get_int(g, 'ID'),
                    'error':  get_int(g, 'ERROR'),
                    'name':   get_text(g, 'W_NAME'),
                    'status': get_int(g, 'STATUS'),
                })

        return cls(
            status        = get_int(elem, 'STATUS'),
            waybill_id    = get_int(elem, 'ID'),
            goods_results = goods_results,
        )


@dataclass
class WayBillListItem:
    """Summary record from a waybill list query."""

    id: int = 0
    waybill_type: int = 0
    create_date: str = ''
    buyer_tin: str = ''
    buyer_name: str = ''
    seller_tin: str = ''
    seller_name: str = ''
    start_address: str = ''
    end_address: str = ''
    driver_tin: str = ''
    transport_cost: float = 0
    reception_info: str = ''
    receiver_info: str = ''
    delivery_date: str = ''
    status: int = 0
    activate_date: str = ''
    parent_id: str = ''
    full_amount: float = 0
    car_number: str = ''
    waybill_number: str = ''
    close_date: str = ''
    s_user_id: int = 0
    begin_date: str = ''
    comment: str = ''
    buyer_status: int = 0
    seller_status: int = 0
    is_confirmed: int = 0

    @classmethod
    def from_xml(cls, elem: ET.Element) -> WayBillListItem:
        """Parse a WAYBILL element from a list response."""
        return cls(
            id             = get_int(elem, 'ID'),
            waybill_type   = get_int(elem, 'TYPE'),
            create_date    = get_text(elem, 'CREATE_DATE'),
            buyer_tin      = get_text(elem, 'BUYER_TIN'),
            buyer_name     = get_text(elem, 'BUYER_NAME'),
            seller_tin     = get_text(elem, 'SELLER_TIN'),
            seller_name    = get_text(elem, 'SELLER_NAME'),
            start_address  = get_text(elem, 'START_ADDRESS'),
            end_address    = get_text(elem, 'END_ADDRESS'),
            driver_tin     = get_text(elem, 'DRIVER_TIN'),
            transport_cost = get_decimal(elem, 'TRANSPORT_COAST'),
            reception_info = get_text(elem, 'RECEPTION_INFO'),
            receiver_info  = get_text(elem, 'RECEIVER_INFO'),
            delivery_date  = get_text(elem, 'DELIVERY_DATE'),
            status         = get_int(elem, 'STATUS'),
            activate_date  = get_text(elem, 'ACTIVATE_DATE'),
            parent_id      = get_text(elem, 'PAR_ID'),
            full_amount    = get_decimal(elem, 'FULL_AMOUNT'),
            car_number     = get_text(elem, 'CAR_NUMBER'),
            waybill_number = get_text(elem, 'WAYBILL_NUMBER'),
            close_date     = get_text(elem, 'CLOSE_DATE'),
            s_user_id      = get_int(elem, 'S_USER_ID'),
            begin_date     = get_text(elem, 'BEGIN_DATE'),
            comment        = get_text(elem, 'WAYBILL_COMMENT'),
            buyer_status   = get_int(elem, 'BUYER_ST'),
            seller_status  = get_int(elem, 'SELLER_ST'),
            is_confirmed   = get_int(elem, 'IS_CONFIRMED'),
        )
