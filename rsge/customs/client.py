"""Client for the RS.ge Customs Declarations REST API.

This API provides access to assessed customs declarations data
using OAuth2-style bearer token authentication.
"""

from __future__ import annotations

from typing import Any

import requests

from rsge.core.exceptions import (
    RSGeAPIError,
    RSGeAuthenticationError,
    RSGeConnectionError,
)
from rsge.customs.models import CustomsAuthResponse, CustomsDeclaration

_DEFAULT_BASE_URL = 'https://services.rs.ge'


class CustomsClient:
    """Client for the RS.ge Customs Declarations REST API.

    Supports both one-factor and two-factor authentication flows.

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

    def authenticate(
        self,
        username: str,
        password: str,
        device_code: str = '',
    ) -> CustomsAuthResponse:
        """Authenticate with the customs API (one-factor).

        Args:
            username: Portal username.
            password: Portal password.
            device_code: Optional device identifier.

        Returns:
            CustomsAuthResponse with the access token.

        Raises:
            RSGeAuthenticationError: If credentials are invalid.
        """
        payload: dict[str, str] = {
            'USERNAME': username,
            'PASSWORD': password,
        }
        if device_code:
            payload['DEVICE_CODE'] = device_code

        data = self._post('/Authenticate', payload)
        response = CustomsAuthResponse.from_dict(data)

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
        save_device: bool = False,
        address: str = '',
        browser: str = '',
        oper_system: str = '',
    ) -> CustomsAuthResponse:
        """Complete two-factor authentication with a PIN.

        Args:
            pin_token: Token from the first authentication step.
            pin: The PIN code sent to the user.
            device_code: Device identifier.
            save_device: Whether to remember this device.
            address: Client IP/address (for device saving).
            browser: Browser identifier.
            oper_system: OS identifier.

        Returns:
            CustomsAuthResponse with the access token.
        """
        payload: dict[str, str] = {
            'PIN_TOKEN': pin_token,
            'PIN': pin,
            'DEVICE_CODE': device_code,
            'ADDRESS': address,
            'BROWSER': browser,
            'OPER_SYSTEM': oper_system,
        }

        data = self._post('/AuthenticatePin', payload)
        response = CustomsAuthResponse.from_dict(data)

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
            self._post('/SignOut', {})
        except RSGeAPIError:
            pass

        self._access_token = ''
        self._session.headers.pop('Authorization', None)
        return True

    def get_declarations(
        self,
        date_from: str,
        date_to: str,
    ) -> list[CustomsDeclaration]:
        """Retrieve assessed customs declarations for a date range.

        Args:
            date_from: Start date (ISO format).
            date_to: End date.

        Returns:
            List of CustomsDeclaration objects.

        Raises:
            RSGeAuthenticationError: If not authenticated.
            RSGeAPIError: On API errors.
        """
        if not self._access_token:
            raise RSGeAuthenticationError('Not authenticated. Call authenticate() first.')

        params = {'dateFrom': date_from, 'dateTo': date_to}

        try:
            response = self._session.get(
                f'{self._base_url}/GetAsycudaDeclarations',
                params  = params,
                timeout = self._timeout,
            )

            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise RSGeConnectionError(f'Connection failed: {exc}') from exc
        except requests.exceptions.HTTPError as exc:
            raise RSGeAPIError(f'HTTP error: {exc.response.status_code}') from exc

        data = response.json()
        status = data.get('STATUS', {})
        if status.get('CODE', 0) != 0:
            raise RSGeAPIError(
                f"API error: {status.get('MESSAGE', 'Unknown error')}",
                code=status.get('CODE'),
            )

        items = data.get('DATA', [])
        if isinstance(items, list):
            return [CustomsDeclaration.from_dict(item) for item in items]
        return []

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request and return the parsed JSON response.

        Args:
            path: API endpoint path.
            payload: JSON request body.

        Returns:
            Parsed response dict.
        """
        try:
            response = self._session.post(
                f'{self._base_url}{path}',
                json    = payload,
                timeout = self._timeout,
            )

            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise RSGeConnectionError(f'Connection failed: {exc}') from exc
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response else 0
            raise RSGeAPIError(f'HTTP error: {status_code}') from exc

        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> CustomsClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
