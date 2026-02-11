"""Client for the RS.ge eAPI Invoice/Declaration REST service.

This API provides access to tax invoice (საგადასახადო დოკუმენტი)
operations using OAuth2-style bearer token authentication.

Base URL: https://eapi.rs.ge
"""

from __future__ import annotations

import uuid
from typing import Any

import requests

from rsge.core.exceptions import (
    RSGeAPIError,
    RSGeAuthenticationError,
    RSGeConnectionError,
)
from rsge.invoice.models import (
    BarCode,
    Invoice,
    InvoiceAction,
    InvoiceAuthResponse,
    OrgInfo,
    TransactionResult,
    Unit,
)

_DEFAULT_BASE_URL = 'https://eapi.rs.ge'


class InvoiceClient:
    """Client for the RS.ge eAPI Invoice/Declaration service.

    Supports one-factor and two-factor authentication flows.

    Args:
        base_url: API base URL.
        timeout: HTTP request timeout in seconds.
        verify_ssl: Whether to verify SSL certificates.
    """

    def __init__(
        self,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        self._base_url = base_url.rstrip('/')
        self._timeout = timeout
        self._session = requests.Session()
        self._session.verify = verify_ssl
        self._session.headers.update({'Content-Type': 'application/json'})
        self._access_token: str = ''

    @property
    def is_authenticated(self) -> bool:
        """Whether an access token is currently set."""
        return bool(self._access_token)

    # ── Authentication ───────────────────────────────────────────

    def authenticate(
        self,
        username: str,
        password: str,
        device_code: str = '',
    ) -> InvoiceAuthResponse:
        """Authenticate with the eAPI (one-factor or first step of two-factor).

        Args:
            username: Portal username.
            password: Portal password.
            device_code: Optional device identifier GUID.

        Returns:
            InvoiceAuthResponse (check .needs_pin for two-factor flow).

        Raises:
            RSGeAuthenticationError: If credentials are invalid.
        """
        payload: dict[str, Any] = {
            'USERNAME': username,
            'PASSWORD': password,
        }
        if device_code:
            payload['DEVICE_CODE'] = device_code

        data = self._auth_post('/Users/Authenticate', payload)
        response = InvoiceAuthResponse.from_dict(data)

        if response.access_token:
            self._access_token = response.access_token
            self._session.headers['Authorization'] = f'bearer {response.access_token}'

        return response

    def authenticate_pin(
        self,
        pin_token: str,
        pin: str,
        device_code: str = '',
        *,
        address: str = '',
        browser: str = '',
        oper_system: str = '',
    ) -> InvoiceAuthResponse:
        """Complete two-factor authentication with a PIN.

        Args:
            pin_token: Token from the first authentication step.
            pin: The PIN code sent to the user's phone.
            device_code: Device identifier GUID.
            address: Client IP/address.
            browser: Browser identifier.
            oper_system: OS identifier.

        Returns:
            InvoiceAuthResponse with the access token.
        """
        payload: dict[str, Any] = {
            'PIN_TOKEN': pin_token,
            'PIN': pin,
            'DEVICE_CODE': device_code if device_code else None,
            'ADDRESS': address if address else None,
            'BROWSER': browser if browser else None,
            'OPER_SYSTEM': oper_system if oper_system else None,
        }

        data = self._auth_post('/Users/AuthenticatePin', payload)
        response = InvoiceAuthResponse.from_dict(data)

        if response.access_token:
            self._access_token = response.access_token
            self._session.headers['Authorization'] = f'bearer {response.access_token}'

        return response

    def sign_out(self) -> bool:
        """Sign out and invalidate the current access token.

        Returns:
            True if sign-out succeeded.
        """
        if not self._access_token:
            return True

        try:
            self._auth_post('/Users/SignOut', {})
        except (RSGeAPIError, RSGeConnectionError):
            pass

        self._access_token = ''
        self._session.headers.pop('Authorization', None)
        return True

    # ── Common / Reference ───────────────────────────────────────

    def get_vat_payer_status(self, tin: str, vat_date: str = '') -> bool:
        """Check if an organization is a VAT payer.

        Note:
            This endpoint returns 500 on the RS.ge sandbox environment.
            Use ``get_org_info(tin).is_vat_payer`` as an alternative.

        Args:
            tin: Tax identification number (9 or 11 digits).
            vat_date: Optional date for historical check.

        Returns:
            True if the organization is a VAT payer.
        """
        self._require_auth()
        payload: dict[str, Any] = {'Tin': tin}
        if vat_date:
            payload['VatDate'] = vat_date
        data = self._post('/Org/GetVatPayerStatus', payload)
        return bool(data.get('DATA', {}).get('IsVatPayer', False))

    def get_org_info(self, tin: str) -> OrgInfo:
        """Get organization info by TIN.

        Args:
            tin: Tax identification number.

        Returns:
            OrgInfo object.
        """
        self._require_auth()
        data = self._post('/Org/GetOrgInfoByTin', {'Tin': tin})
        return OrgInfo.from_dict(data.get('DATA', {}))

    def get_units(self) -> list[Unit]:
        """Get available measurement units.

        Returns:
            List of Unit objects.
        """
        self._require_auth()
        data = self._post('/Common/GetUnits', {})
        items = data.get('DATA', [])
        if isinstance(items, list):
            return [Unit.from_dict(item) for item in items]
        return []

    def get_transaction_result(self, transaction_id: str) -> TransactionResult:
        """Get the result of an async save transaction.

        Args:
            transaction_id: The transaction UUID.

        Returns:
            TransactionResult with the invoice ID.
        """
        self._require_auth()
        data = self._post('/Common/GetTransactionResult', {'TransactionId': transaction_id})
        return TransactionResult.from_dict(data.get('DATA', {}))

    # ── Invoice CRUD ─────────────────────────────────────────────

    def get_actions(self) -> list[InvoiceAction]:
        """Get available invoice statuses/actions.

        Returns:
            List of InvoiceAction objects.
        """
        self._require_auth()
        data = self._post('/Invoice/GetActions', {})
        items = data.get('DATA', [])
        if isinstance(items, list):
            return [InvoiceAction.from_dict(item) for item in items]
        return []

    def get_invoice(
        self,
        invoice_id: int = 0,
        invoice_number: int = 0,
        parent_invoice_id: int = 0,
    ) -> Invoice:
        """Get a specific invoice by ID or number.

        Args:
            invoice_id: Invoice identification number.
            invoice_number: Invoice number.
            parent_invoice_id: Parent invoice ID (for distribution sub-invoices).

        Returns:
            Invoice object.
        """
        self._require_auth()
        payload: dict[str, Any] = {
            'InvoiceID': invoice_id,
            'InvoiceNumber': invoice_number,
            'parentInvoiceID': parent_invoice_id,
        }
        data = self._post('/Invoice/GetInvoice', payload)
        invoice_data = data.get('DATA', {}).get('INVOICE', {})
        return Invoice.from_dict(invoice_data)

    def save_invoice(
        self,
        invoice: Invoice,
        transaction_id: str = '',
    ) -> str:
        """Save (create or update) an invoice.

        For new invoices, set ID=0. For corrections, set PREV_CORRECTION_ID.

        Args:
            invoice: Invoice object to save.
            transaction_id: Optional transaction UUID. Auto-generated if empty.

        Returns:
            The transaction ID used (for GetTransactionResult polling).
        """
        self._require_auth()
        if not transaction_id:
            transaction_id = str(uuid.uuid4())

        payload: dict[str, Any] = {
            'INVOICE': invoice.to_dict(),
            'TransactionId': transaction_id,
        }
        self._post('/Invoice/SaveInvoice', payload)
        return transaction_id

    def activate_invoice(
        self,
        invoice: Invoice,
        transaction_id: str = '',
    ) -> str:
        """Activate an invoice (send for registration).

        The invoice object should contain at minimum the ID field.
        If SELLER_ACTION should be set to 1, update it before calling.

        Args:
            invoice: Invoice object (can be minimal with just ID).
            transaction_id: Optional transaction UUID. Auto-generated if empty.

        Returns:
            The transaction ID used.
        """
        self._require_auth()
        if not transaction_id:
            transaction_id = str(uuid.uuid4())

        payload: dict[str, Any] = {
            'INVOICE': invoice.to_dict(),
            'TransactionId': transaction_id,
        }
        self._post('/Invoice/ActivateInvoice', payload)
        return transaction_id

    def activate_invoices(self, invoice_ids: list[int]) -> bool:
        """Activate multiple invoices at once.

        Args:
            invoice_ids: List of invoice IDs to activate.

        Returns:
            True on success.
        """
        self._require_auth()
        invoices = [{'ID': id_} for id_ in invoice_ids]
        self._post('/Invoice/ActivateInvoices', {'Invoices': invoices})
        return True

    def delete_invoice(self, invoice_id: int) -> bool:
        """Delete a saved (draft) invoice.

        Args:
            invoice_id: Invoice ID to delete.

        Returns:
            True on success.
        """
        self._require_auth()
        self._post('/Invoice/DeleteInvoice', {'INVOICE': {'ID': invoice_id}})
        return True

    def cancel_invoice(self, invoice_id: int) -> bool:
        """Cancel an active/confirmed invoice (request cancellation).

        Args:
            invoice_id: Invoice ID to cancel.

        Returns:
            True on success.
        """
        self._require_auth()
        self._post('/Invoice/CancelInvoice', {'INVOICE': {'ID': invoice_id}})
        return True

    def refuse_invoice(self, invoice_id: int) -> bool:
        """Refuse a received invoice (as buyer).

        Args:
            invoice_id: Invoice ID to refuse.

        Returns:
            True on success.
        """
        self._require_auth()
        self._post('/Invoice/RefuseInvoice', {'INVOICE': {'ID': invoice_id}})
        return True

    def refuse_invoices(self, invoice_ids: list[int]) -> bool:
        """Refuse multiple invoices at once (as buyer).

        Args:
            invoice_ids: List of invoice IDs to refuse.

        Returns:
            True on success.
        """
        self._require_auth()
        invoices = [{'ID': id_} for id_ in invoice_ids]
        self._post('/Invoice/RefuseInvoices', {'Invoices': invoices})
        return True

    def confirm_invoice(self, invoice_id: int) -> bool:
        """Confirm a received invoice (as buyer).

        Args:
            invoice_id: Invoice ID to confirm.

        Returns:
            True on success.
        """
        self._require_auth()
        self._post('/Invoice/ConfirmInvoice', {'INVOICE': {'ID': invoice_id}})
        return True

    def confirm_invoices(self, invoice_ids: list[int]) -> bool:
        """Confirm multiple invoices at once (as buyer).

        Args:
            invoice_ids: List of invoice IDs to confirm.

        Returns:
            True on success.
        """
        self._require_auth()
        invoices = [{'ID': id_} for id_ in invoice_ids]
        self._post('/Invoice/ConfirmInvoices', {'Invoices': invoices})
        return True

    def list_invoices(self, **filters: Any) -> list[Invoice]:
        """List invoices with optional filters.

        Supported filter keys (all optional):
            ID, INV_NUMBER, PARENT_INV_NUMBER, INV_CATEGORY, INV_TYPE,
            ACTION, CREATE_DATE, CHANGE_DATE, OPERATION_DATE, ACTIVATE_DATE,
            CONFIRM_DATE, REFUSE_DATE, DELIVERY_DATE, REQUEST_CANCEL_DATE,
            AGREE_CANCEL_DATE, CORRECT_DATE, TRANS_START_DATE, TRANS_NAME,
            TRANS_COMPANY, TRANS_DRIVER, TRANS_CAR_MODEL, TRANS_CAR_NO,
            TRANS_TRAILER_NO, TRANS_COST, TRANS_COST_PAYER,
            SELLER_ACTION_TXT, BUYER_ACTION_TXT, SELLER, BUYER,
            TIN_BUYER, DECL_OPERATION_PERIOD, MAXIMUM_ROWS, TYPE

        Returns:
            List of Invoice objects parsed from the Fields/Rows response.
        """
        self._require_auth()
        data = self._post('/Invoice/ListInvoices', filters)

        data_obj = data.get('DATA', {})
        inner = data_obj.get('Data', {})
        fields = inner.get('Fields', [])
        rows = inner.get('Rows', [])

        result: list[Invoice] = []
        for row in rows:
            row_dict = dict(zip(fields, row))
            result.append(Invoice.from_dict(row_dict))

        return result

    def list_goods(self, invoice_ids: list[int]) -> list[Invoice]:
        """List goods for one or more invoices.

        Args:
            invoice_ids: List of invoice IDs.

        Returns:
            List of Invoice objects with their goods populated.
        """
        self._require_auth()
        invoices_param = [{'ID': id_} for id_ in invoice_ids]
        data = self._post('/Invoice/ListGoods', {'Invoices': invoices_param})

        invoices_data = data.get('DATA', {}).get('INVOICES', [])
        result: list[Invoice] = []
        for item in invoices_data:
            inv_data = item.get('INVOICE', {})
            result.append(Invoice.from_dict(inv_data))

        return result

    def list_excise(
        self,
        product_name: str = '',
        effect_date: str = '',
        end_date: str = '',
        maximum_rows: int = 10,
    ) -> list[dict[str, Any]]:
        """List excise product information.

        Args:
            product_name: Filter by product name.
            effect_date: Effect date range (DD-MM-YYYY:DD-MM-YYYY).
            end_date: End date range (DD-MM-YYYY:DD-MM-YYYY).
            maximum_rows: Max rows to return (0=all, default 10).

        Returns:
            List of excise row dicts (Fields/Rows format parsed).
        """
        self._require_auth()
        payload: dict[str, Any] = {}
        if product_name:
            payload['PRODUCT_NAME'] = product_name
        if effect_date:
            payload['EFFECT_DATE'] = effect_date
        if end_date:
            payload['END_DATE'] = end_date
        if maximum_rows != 10:
            payload['MAXIMUM_ROWS'] = maximum_rows

        data = self._post('/Invoice/ListExcise', payload)
        data_obj = data.get('DATA', {})
        inner = data_obj.get('Data', {})
        fields = inner.get('Fields', [])
        rows = inner.get('Rows', [])

        return [dict(zip(fields, row)) for row in rows]

    def list_bar_codes(
        self,
        barcode: str = '',
        goods_name: str = '',
        unit_txt: str = '',
        vat_type_txt: str = '',
        unit_price: float | None = None,
        maximum_rows: int = 10,
    ) -> list[BarCode]:
        """List barcode catalog entries.

        Args:
            barcode: Filter by barcode.
            goods_name: Filter by product name.
            unit_txt: Filter by unit text.
            vat_type_txt: Filter by VAT type text.
            unit_price: Filter by unit price.
            maximum_rows: Max rows (0=all, default 10).

        Returns:
            List of BarCode objects.
        """
        self._require_auth()
        payload: dict[str, Any] = {}
        if barcode:
            payload['BARCODE'] = barcode
        if goods_name:
            payload['GOODS_NAME'] = goods_name
        if unit_txt:
            payload['UNIT_TXT'] = unit_txt
        if vat_type_txt:
            payload['VAT_TYPE_TXT'] = vat_type_txt
        if unit_price is not None:
            payload['UNIT_PRICE'] = unit_price
        if maximum_rows != 10:
            payload['MAXIMUM_ROWS'] = maximum_rows

        data = self._post('/Invoice/ListBarCodes', payload)
        data_obj = data.get('DATA', {})
        inner = data_obj.get('Data', {})
        fields = inner.get('Fields', [])
        rows = inner.get('Rows', [])

        result: list[BarCode] = []
        for row in rows:
            row_dict = dict(zip(fields, row))
            result.append(BarCode.from_dict(row_dict))
        return result

    def get_bar_code(self, barcode: str) -> BarCode:
        """Get info for a specific barcode.

        Args:
            barcode: The barcode value to look up.

        Returns:
            BarCode object.
        """
        self._require_auth()
        data = self._post('/Invoice/GetBarCode', {'barCode': barcode})
        result_data = data.get('DATA', {}).get('RESULT', {})
        return BarCode.from_dict(result_data)

    def clear_bar_codes(self) -> bool:
        """Clear the internal barcode catalog cache.

        Returns:
            True on success.
        """
        self._require_auth()
        self._post('/Invoice/ClearBarCodes', {})
        return True

    def get_seq_num(self, year: int, month: int | None = None) -> str:
        """Get the declaration sequence number for a period.

        Args:
            year: Year (e.g. 2019).
            month: Optional month (1-12). If omitted, returns yearly.

        Returns:
            Sequence number as string.
        """
        self._require_auth()
        period = str(year)
        if month is not None:
            period += f'{month:02d}'
        data = self._post('/Invoice/GetSeqNum', {'OperationPeriod': period})
        return str(data.get('DATA', {}).get('SeqNum', ''))

    def create_decl(
        self,
        invoice_ids: list[int],
        year: int,
        month: int | None = None,
    ) -> bool:
        """Attach invoices to a declaration for a period.

        Args:
            invoice_ids: List of invoice IDs to attach.
            year: Declaration year.
            month: Optional declaration month.

        Returns:
            True on success.
        """
        self._require_auth()
        period = str(year)
        if month is not None:
            period += f'{month:02d}'

        invoices = [{'ID': id_} for id_ in invoice_ids]
        self._post('/Invoice/CreateDecl', {
            'Invoices': invoices,
            'OperationPeriod': period,
        })
        return True

    # ── Internal helpers ─────────────────────────────────────────

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST with automatic eAPI status check.

        Raises RSGeAPIError if STATUS.ID < 0.
        """
        result = self._raw_post(path, payload)
        self._check_status(result)
        return result

    def _auth_post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST for auth endpoints (no auto status check)."""
        result = self._raw_post(path, payload)
        status = result.get('STATUS', {})
        status_id = int(status.get('ID', 0) or 0)
        if status_id < 0:
            raise RSGeAuthenticationError(
                str(status.get('TEXT', 'Authentication failed')),
                code=status_id,
            )
        return result

    def _raw_post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request and return the parsed JSON response."""
        try:
            response = self._session.post(
                f'{self._base_url}{path}',
                json=payload,
                timeout=self._timeout,
            )
            response.raise_for_status()

        except requests.exceptions.ConnectionError as exc:
            raise RSGeConnectionError(f'Connection failed: {exc}') from exc

        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else 0
            if status_code == 401:
                raise RSGeAuthenticationError(
                    'Unauthorized. Token may be expired.',
                    code=status_code,
                ) from exc
            message = f'HTTP error: {status_code}'
            if exc.response is not None:
                try:
                    body = exc.response.json()
                    api_text = body.get('STATUS', {}).get('TEXT', '')
                    if api_text:
                        message = api_text
                except (ValueError, KeyError):
                    pass
            raise RSGeAPIError(message, code=status_code) from exc

        result: dict[str, Any] = response.json()
        return result

    def _check_status(self, result: dict[str, Any]) -> None:
        """Validate eAPI response status (STATUS.ID < 0 is an error)."""
        status = result.get('STATUS', {})
        status_id = int(status.get('ID', 0) or 0)
        if status_id < 0:
            raise RSGeAPIError(
                str(status.get('TEXT', 'Unknown error')),
                code=status_id,
            )

    def _require_auth(self) -> None:
        """Guard: raise if not authenticated."""
        if not self._access_token:
            raise RSGeAuthenticationError('Not authenticated. Call authenticate() first.')

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> InvoiceClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
