"""High-level client for the RS.ge WayBill SOAP service.

Provides WayBillClient, the primary interface for all electronic
waybill operations against the Georgian Revenue Service.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from rsge.core.exceptions import (
    RSGeAPIError,
    RSGeAuthenticationError,
    RSGePermissionError,
)
from rsge.core.transport import SOAPTransport
from rsge.core.xml_utils import element_to_string, get_int, get_text
from rsge.waybill.enums import (
    CategoryType,
    TransportCostPayer,
    WayBillType,
)
from rsge.waybill.models import (
    AkcizCode,
    ErrorCode,
    ServiceUser,
    TransportType,
    WayBill,
    WayBillListItem,
    WayBillSaveResult,
    WayBillTypeInfo,
    WayBillUnit,
    WoodType,
)

_DEFAULT_URL = 'https://services.rs.ge/WayBillService/WayBillService.asmx'


def _format_dt(dt: datetime | str) -> str:
    """Format a datetime to the ISO string expected by RS.ge."""
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%S')
    return dt


class WayBillClient:
    """Client for the RS.ge electronic waybill SOAP service.

    Args:
        service_user: Service username (su parameter).
        service_password: Service password (sp parameter).
        base_url: SOAP endpoint URL.
        timeout: HTTP request timeout in seconds.
        verify_ssl: Whether to verify SSL certificates.
    """

    def __init__(
        self,
        service_user: str,
        service_password: str,
        base_url: str = _DEFAULT_URL,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        self._su = service_user
        self._sp = service_password
        self._transport = SOAPTransport(
            base_url   = base_url,
            timeout    = timeout,
            verify_ssl = verify_ssl,
        )

    def _auth_params(self) -> dict[str, str]:
        """Return standard authentication parameters."""
        return {'su': self._su, 'sp': self._sp}

    def _call(
        self,
        method: str,
        extra_params: dict[str, Any] | None = None,
        xml_params: dict[str, str] | None = None,
    ) -> Any:
        """Make an authenticated SOAP call."""
        params = self._auth_params()
        if extra_params:
            params.update(extra_params)
        return self._transport.call(method, params=params, xml_params=xml_params)

    def _check_error_code(self, code: int, context: str = '') -> None:
        """Raise appropriate exception for known error codes."""
        if code == -100:
            raise RSGeAuthenticationError(
                f'Invalid service credentials. {context}', code=code,
            )

        if code == -101:
            raise RSGePermissionError(
                f"Permission denied: cannot modify another user's waybill. {context}",
                code=code,
            )

        if code < 0:
            raise RSGeAPIError(f'API error {code}. {context}', code=code)

    def _waybill_filter_params(
        self,
        types: str,
        statuses: str,
        car_number: str,
        begin_date_s: str,
        begin_date_e: str,
        create_date_s: str,
        create_date_e: str,
        driver_tin: str,
        delivery_date_s: str,
        delivery_date_e: str,
        full_amount: str,
        waybill_number: str,
        close_date_s: str,
        close_date_e: str,
        s_user_ids: str,
        comment: str,
    ) -> dict[str, Any]:
        """Build common filter parameters for waybill list queries."""
        return {
            'itypes': types,
            'statuses': statuses,
            'car_number': car_number,
            'begin_date_s': begin_date_s,
            'begin_date_e': begin_date_e,
            'create_date_s': create_date_s,
            'create_date_e': create_date_e,
            'driver_tin': driver_tin,
            'delivery_date_s': delivery_date_s,
            'delivery_date_e': delivery_date_e,
            'full_amount': full_amount,
            'waybill_number': waybill_number,
            'close_date_s': close_date_s,
            'close_date_e': close_date_e,
            's_user_ids': s_user_ids,
            'comment': comment,
        }

    def update_service_user(
        self, user_name: str, user_password: str, ip: str, name: str,
    ) -> bool:
        """Update a service user's registration.

        Args:
            user_name: Declarant portal username.
            user_password: Declarant portal password.
            ip: Whitelisted IP address for API access.
            name: Object / store name.

        Returns:
            True if updated successfully.
        """
        result = self._call('update_service_user', extra_params={
            'user_name': user_name,
            'user_password': user_password,
            'ip': ip,
            'name': name,
        })

        return str(getattr(result, 'text', '')).lower() == 'true'

    def get_service_users(self, user_name: str, user_password: str) -> list[ServiceUser]:
        """List all service users under the given declarant account.

        Args:
            user_name: Declarant portal username.
            user_password: Declarant portal password.

        Returns:
            List of ServiceUser objects.
        """
        result = self._transport.call('get_service_users', params={
            'user_name': user_name, 'user_password': user_password,
        })

        return [ServiceUser.from_xml(e) for e in result.iter('ServiceUser')]

    def check_service_user(self) -> tuple[int, int]:
        """Verify service credentials and return account identifiers.

        Returns:
            Tuple of (un_id, s_user_id).

        Raises:
            RSGeAuthenticationError: If credentials are invalid.
        """
        result = self._call('chek_service_user')
        un_id = get_int(result, 'un_id', 0)
        s_user_id = get_int(result, 's_user_id', 0)
        if un_id == 0 and s_user_id == 0:
            text = getattr(result, 'text', '') or ''
            if text.lower() == 'false':
                raise RSGeAuthenticationError('Invalid service credentials')
        return un_id, s_user_id

    def get_akciz_codes(self) -> list[AkcizCode]:
        """Retrieve excise (akciz) commodity codes."""
        result = self._call('get_akciz_codes')
        return [AkcizCode.from_xml(e) for e in result.iter('AKCIZ_CODE')]

    def get_waybill_types(self) -> list[WayBillTypeInfo]:
        """Retrieve waybill type reference list."""
        result = self._call('get_waybill_types')
        return [WayBillTypeInfo.from_xml(e) for e in result.iter('WAYBILL_TYPE')]

    def get_waybill_units(self) -> list[WayBillUnit]:
        """Retrieve measurement unit reference list."""
        result = self._call('get_waybill_units')
        return [WayBillUnit.from_xml(e) for e in result.iter('WAYBILL_UNIT')]

    def get_transport_types(self) -> list[TransportType]:
        """Retrieve transportation type reference list."""
        result = self._call('get_trans_types')
        return [TransportType.from_xml(e) for e in result.iter('TRANSPORT_TYPE')]

    def get_wood_types(self) -> list[WoodType]:
        """Retrieve wood/timber type reference list."""
        result = self._call('get_wood_types')
        return [WoodType.from_xml(e) for e in result.iter('WOOD_TYPES')]

    def get_error_codes(self) -> list[ErrorCode]:
        """Retrieve API error codes and descriptions."""
        result = self._call('get_error_codes')
        return [ErrorCode.from_xml(e) for e in result.iter('WAYBILL_TYPE')]

    def get_name_from_tin(self, tin: str) -> str:
        """Look up a taxpayer's name by TIN or personal number.

        Args:
            tin: Identification or personal number.

        Returns:
            The registered name.
        """
        result = self._call('get_name_from_tin', extra_params={'tin': tin})
        return result.text or ''

    def create_waybill(
        self,
        waybill_type: WayBillType | int = WayBillType.TRANSPORTATION,
        buyer_tin: str = '',
        buyer_name: str = '',
        start_address: str = '',
        end_address: str = '',
        *,
        check_buyer_tin: int = 1,
        driver_tin: str = '',
        check_driver_tin: int = 1,
        driver_name: str = '',
        car_number: str = '',
        transport_cost: float = 0,
        transport_cost_payer: TransportCostPayer | int = TransportCostPayer.SELLER,
        transport_type_id: int = 1,
        transport_type_txt: str = '',
        comment: str = '',
        category: CategoryType | int = CategoryType.REGULAR,
        is_medicine: int = 0,
        parent_id: str = '',
        transporter_tin: str = '',
    ) -> WayBill:
        """Create a new waybill object in memory (does not save to server).

        Returns:
            A new WayBill instance.
        """
        return WayBill(
            waybill_type         = waybill_type,
            buyer_tin            = buyer_tin,
            check_buyer_tin      = check_buyer_tin,
            buyer_name           = buyer_name,
            start_address        = start_address,
            end_address          = end_address,
            driver_tin           = driver_tin,
            check_driver_tin     = check_driver_tin,
            driver_name          = driver_name,
            car_number           = car_number,
            transport_cost       = transport_cost,
            transport_cost_payer = transport_cost_payer,
            transport_type_id    = transport_type_id,
            transport_type_txt   = transport_type_txt,
            comment              = comment,
            category             = category,
            is_medicine          = is_medicine,
            parent_id            = parent_id,
            transporter_tin      = transporter_tin,
        )

    def save_waybill(self, waybill: WayBill) -> WayBillSaveResult:
        """Save (create or update) a waybill on the RS.ge server.

        Args:
            waybill: The waybill to save. Set id=0 for new.

        Returns:
            A WayBillSaveResult with status and assigned ID.
        """
        xml_str = element_to_string(waybill.to_xml())
        result = self._call('save_waybill', xml_params={'waybill': xml_str})
        return WayBillSaveResult.from_xml(result)

    def get_waybill(self, waybill_id: int) -> WayBill:
        """Retrieve a single waybill by its ID.

        Args:
            waybill_id: The waybill's unique ID.

        Returns:
            A fully populated WayBill instance.
        """
        result = self._call('get_waybill', extra_params={'waybill_id': waybill_id})
        return WayBill.from_xml(result)

    def get_waybills(
        self,
        *,
        types: str = '',
        buyer_tin: str = '',
        statuses: str = '',
        car_number: str = '',
        begin_date_s: str = '',
        begin_date_e: str = '',
        create_date_s: str = '',
        create_date_e: str = '',
        driver_tin: str = '',
        delivery_date_s: str = '',
        delivery_date_e: str = '',
        full_amount: str = '',
        waybill_number: str = '',
        close_date_s: str = '',
        close_date_e: str = '',
        s_user_ids: str = '',
        comment: str = '',
    ) -> list[WayBillListItem]:
        """List seller-side waybills with optional filters.

        Returns:
            List of WayBillListItem objects.
        """
        params = self._waybill_filter_params(
            types, statuses, car_number, begin_date_s, begin_date_e,
            create_date_s, create_date_e, driver_tin, delivery_date_s,
            delivery_date_e, full_amount, waybill_number, close_date_s,
            close_date_e, s_user_ids, comment,
        )

        params['buyer_tin'] = buyer_tin
        result = self._call('get_waybills', extra_params=params)
        return [WayBillListItem.from_xml(e) for e in result.iter('WAYBILL')]

    def get_buyer_waybills(
        self,
        *,
        types: str = '',
        seller_tin: str = '',
        statuses: str = '',
        car_number: str = '',
        begin_date_s: str = '',
        begin_date_e: str = '',
        create_date_s: str = '',
        create_date_e: str = '',
        driver_tin: str = '',
        delivery_date_s: str = '',
        delivery_date_e: str = '',
        full_amount: str = '',
        waybill_number: str = '',
        close_date_s: str = '',
        close_date_e: str = '',
        s_user_ids: str = '',
        comment: str = '',
    ) -> list[WayBillListItem]:
        """List buyer-side waybills with optional filters.

        Returns:
            List of WayBillListItem objects.
        """
        params = self._waybill_filter_params(
            types, statuses, car_number, begin_date_s, begin_date_e,
            create_date_s, create_date_e, driver_tin, delivery_date_s,
            delivery_date_e, full_amount, waybill_number, close_date_s,
            close_date_e, s_user_ids, comment,
        )

        params['seller_tin'] = seller_tin
        result = self._call('get_buyer_waybills', extra_params=params)
        return [WayBillListItem.from_xml(e) for e in result.iter('WAYBILL')]

    def get_waybills_ex(
        self,
        *,
        types: str = '',
        buyer_tin: str = '',
        statuses: str = '',
        car_number: str = '',
        begin_date_s: str = '',
        begin_date_e: str = '',
        create_date_s: str = '',
        create_date_e: str = '',
        driver_tin: str = '',
        delivery_date_s: str = '',
        delivery_date_e: str = '',
        full_amount: str = '',
        waybill_number: str = '',
        close_date_s: str = '',
        close_date_e: str = '',
        s_user_ids: str = '',
        comment: str = '',
        is_confirmed: int = 0,
    ) -> list[WayBillListItem]:
        """List seller-side waybills with extended filter (includes confirmation status).

        Args:
            is_confirmed: 0 unconfirmed, 1 confirmed, -1 rejected.

        Returns:
            List of WayBillListItem objects.
        """
        params = self._waybill_filter_params(
            types, statuses, car_number, begin_date_s, begin_date_e,
            create_date_s, create_date_e, driver_tin, delivery_date_s,
            delivery_date_e, full_amount, waybill_number, close_date_s,
            close_date_e, s_user_ids, comment,
        )

        params['buyer_tin'] = buyer_tin
        params['is_confirmed'] = is_confirmed
        result = self._call('get_waybills_ex', extra_params=params)
        return [WayBillListItem.from_xml(e) for e in result.iter('WAYBILL')]

    def get_buyer_waybills_ex(
        self,
        *,
        types: str = '',
        seller_tin: str = '',
        statuses: str = '',
        car_number: str = '',
        begin_date_s: str = '',
        begin_date_e: str = '',
        create_date_s: str = '',
        create_date_e: str = '',
        driver_tin: str = '',
        delivery_date_s: str = '',
        delivery_date_e: str = '',
        full_amount: str = '',
        waybill_number: str = '',
        close_date_s: str = '',
        close_date_e: str = '',
        s_user_ids: str = '',
        comment: str = '',
        is_confirmed: int = 0,
    ) -> list[WayBillListItem]:
        """List buyer-side waybills with extended filter (includes confirmation).

        Returns:
            List of WayBillListItem objects.
        """
        params = self._waybill_filter_params(
            types, statuses, car_number, begin_date_s, begin_date_e,
            create_date_s, create_date_e, driver_tin, delivery_date_s,
            delivery_date_e, full_amount, waybill_number, close_date_s,
            close_date_e, s_user_ids, comment,
        )

        params['seller_tin'] = seller_tin
        params['is_confirmed'] = is_confirmed
        result = self._call('get_buyer_waybills_ex', extra_params=params)
        return [WayBillListItem.from_xml(e) for e in result.iter('WAYBILL')]

    def get_waybills_v1(
        self,
        last_update_date_s: str,
        last_update_date_e: str,
        buyer_tin: str = '',
    ) -> list[WayBillListItem]:
        """List waybills by last-update date range (v1 endpoint, max 3 days).

        Args:
            last_update_date_s: Range start.
            last_update_date_e: Range end.
            buyer_tin: Optional company TIN filter.
        """
        result = self._call('get_waybills_v1', extra_params={
            'buyer_tin': buyer_tin,
            'last_update_date_s': last_update_date_s,
            'last_update_date_e': last_update_date_e,
        })

        return [WayBillListItem.from_xml(e) for e in result.iter('WAYBILL')]

    def activate_waybill(self, waybill_id: int) -> str:
        """Activate a waybill (start transportation). Returns waybill number."""
        result = self._call('send_waybill', extra_params={'waybill_id': waybill_id})
        return result.text or ''

    def activate_waybill_with_date(self, waybill_id: int, begin_date: datetime | str) -> str:
        """Activate with specific transport start date. Returns waybill number."""
        result = self._call('send_waybill_vd', extra_params={
            'begin_date': _format_dt(begin_date),
            'waybill_id': waybill_id,
        })

        return result.text or ''

    def close_waybill(self, waybill_id: int) -> int:
        """Close/complete a waybill. Returns 1 on success."""
        result = self._call('close_waybill', extra_params={'waybill_id': waybill_id})
        code = int(result.text or '-1')
        self._check_error_code(code, 'close_waybill')
        return code

    def close_waybill_with_date(self, waybill_id: int, delivery_date: datetime | str) -> int:
        """Close with specific delivery date. Returns 1 on success."""
        result = self._call('close_waybill_vd', extra_params={
            'delivery_date': _format_dt(delivery_date),
            'waybill_id': waybill_id,
        })

        code = int(result.text or '-1')
        self._check_error_code(code, 'close_waybill_vd')
        return code

    def delete_waybill(self, waybill_id: int) -> int:
        """Delete a saved (non-activated) waybill. Returns 1 on success."""
        result = self._call('del_waybill', extra_params={'waybill_id': waybill_id})
        code = int(result.text or '-1')
        self._check_error_code(code, 'del_waybill')
        return code

    def cancel_waybill(self, waybill_id: int) -> int:
        """Cancel (void) an activated waybill. Returns 1 on success."""
        result = self._call('ref_waybill', extra_params={'waybill_id': waybill_id})
        code = int(result.text or '-1')
        self._check_error_code(code, 'ref_waybill')
        return code

    def confirm_waybill(self, waybill_id: int) -> bool:
        """Confirm (accept) a waybill as buyer."""
        result = self._call('confirm_waybill', extra_params={'waybill_id': waybill_id})
        return (result.text or '').lower() == 'true'

    def reject_waybill(self, waybill_id: int) -> bool:
        """Reject a waybill as buyer."""
        result = self._call('reject_waybill', extra_params={'waybill_id': waybill_id})
        return (result.text or '').lower() == 'true'

    def save_waybill_transporter(
        self,
        waybill_id: int,
        car_number: str,
        driver_tin: str,
        driver_name: str,
        *,
        check_driver_tin: int = 1,
        transport_type_id: int = 1,
        transport_type_txt: str = '',
        reception_info: str = '',
        receiver_info: str = '',
    ) -> int:
        """Save transporter-specific fields on a forwarded waybill."""
        result = self._call('save_waybill_transporter', extra_params={
            'waybill_id': waybill_id,
            'car_number': car_number,
            'driver_tin': driver_tin,
            'chek_driver_tin': check_driver_tin,
            'driver_name': driver_name,
            'trans_id': transport_type_id,
            'trans_txt': transport_type_txt,
            'reception_info': reception_info,
            'receiver_info': receiver_info,
        })

        return int(result.text or '-1')

    def activate_waybill_transporter(
        self, waybill_id: int, begin_date: datetime | str,
    ) -> tuple[int, str]:
        """Activate a waybill as transporter. Returns (code, waybill_number)."""
        result = self._call('send_waybill_transporter', extra_params={
            'waybill_id': waybill_id,
            'begin_date': _format_dt(begin_date),
        })

        code = int(get_text(result, '.') or result.text or '-1')
        number = get_text(result, 'waybill_number', '')
        return code, number

    def close_waybill_transporter(
        self,
        waybill_id: int,
        delivery_date: datetime | str,
        reception_info: str = '',
        receiver_info: str = '',
    ) -> int:
        """Close a waybill as transporter."""
        result = self._call('close_waybill_transporter', extra_params={
            'waybill_id': waybill_id,
            'reception_info': reception_info,
            'receiver_info': receiver_info,
            'delivery_date': _format_dt(delivery_date),
        })

        return int(result.text or '-1')

    def save_invoice(self, waybill_id: int, invoice_id: int = 0) -> tuple[int, int]:
        """Issue a tax invoice from a waybill. Returns (code, invoice_id)."""
        result = self._call('save_invoice', extra_params={
            'waybill_id': waybill_id, 'in_inv_id': invoice_id,
        })

        code = int(result.text or '-1')
        out_id = get_int(result, 'out_inv_id', 0)
        self._check_error_code(code, 'save_invoice')
        return code, out_id

    def save_waybill_template(self, name: str, waybill: WayBill) -> int:
        """Save a waybill template. Returns 1 on success."""
        xml_str = element_to_string(waybill.to_xml())
        result = self._call(
            'save_waybill_tamplate',
            extra_params = {'v_name': name},
            xml_params   = {'waybill': xml_str},
        )

        return int(result.text or '-1')

    def get_waybill_templates(self) -> list[dict[str, Any]]:
        """List all saved waybill templates."""
        result = self._call('get_waybill_tamplates')
        templates: list[dict[str, Any]] = []
        for elem in result.iter():
            tid = get_int(elem, 'ID')
            if tid:
                templates.append({'id': tid, 'name': get_text(elem, 'NAME')})
        return templates

    def get_waybill_template(self, template_id: int) -> WayBill:
        """Retrieve a waybill template by ID."""
        result = self._call('get_waybill_tamplate', extra_params={'id': template_id})
        return WayBill.from_xml(result)

    def delete_waybill_template(self, template_id: int) -> int:
        """Delete a waybill template. Returns 1 on success."""
        result = self._call('delete_waybill_tamplate', extra_params={'id': template_id})
        return int(result.text or '-1')

    def save_bar_code(
        self,
        bar_code: str,
        goods_name: str,
        unit_id: int,
        unit_txt: str = '',
        akciz_id: int = 0,
    ) -> int:
        """Save a barcode to personal catalog. Returns 1 on success."""
        result = self._call('save_bar_code', extra_params={
            'bar_code': bar_code,
            'goods_name': goods_name,
            'unit_id': unit_id,
            'unit_txt': unit_txt,
            'a_id': akciz_id,
        })

        return int(result.text or '-1')

    def delete_bar_code(self, bar_code: str) -> int:
        """Delete a barcode. Returns 1 on success."""
        result = self._call('delete_bar_code', extra_params={'bar_code': bar_code})
        return int(result.text or '-1')

    def get_bar_codes(self, bar_code: str = '') -> list[dict[str, Any]]:
        """List barcodes from the personal catalog."""
        result = self._call('get_bar_codes', extra_params={'bar_code': bar_code})
        codes: list[dict[str, Any]] = []
        for elem in result.iter():
            bc = get_text(elem, 'bar_code', '')
            if bc:
                codes.append({
                    'bar_code': bc,
                    'goods_name': get_text(elem, 'goods_name'),
                    'unit_id': get_int(elem, 'unit_id'),
                    'unit_txt': get_text(elem, 'unit_txt'),
                    'a_id': get_int(elem, 'a_id'),
                })

        return codes

    def save_car_number(self, car_number: str) -> int:
        """Register a vehicle for distribution. Returns 1 on success."""
        result = self._call('save_car_numbers', extra_params={'car_number': car_number})
        return int(result.text or '-1')

    def delete_car_number(self, car_number: str) -> int:
        """Remove a registered vehicle. Returns 1 on success."""
        result = self._call('delete_car_numbers', extra_params={'car_number': car_number})
        return int(result.text or '-1')

    def get_car_numbers(self) -> list[str]:
        """List all registered vehicle numbers."""
        result = self._call('get_car_numbers')
        numbers: list[str] = []
        for elem in result.iter():
            text = (elem.text or '').strip()
            if text:
                numbers.append(text)
        return numbers

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._transport.close()

    def __enter__(self) -> WayBillClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
