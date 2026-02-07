"""Low-level SOAP transport for communicating with the RS.ge WayBill service.

Handles HTTP request construction, SOAP envelope wrapping/unwrapping,
and basic error handling at the transport level.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

import requests

from rsge.core.exceptions import RSGeConnectionError

_SOAP_ENVELOPE = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    {body}
  </soap:Body>
</soap:Envelope>'''

_NAMESPACE = 'http://tempuri.org/'


class SOAPTransport:
    """Low-level SOAP client for the RS.ge WayBill web service.

    Args:
        base_url: The WSDL endpoint URL.
        timeout: Request timeout in seconds.
        verify_ssl: Whether to verify SSL certificates.
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        self._base_url = base_url.rstrip('/')
        self._timeout = timeout
        self._session = requests.Session()
        self._session.verify = verify_ssl
        self._session.headers.update({
            'Content-Type': 'text/xml; charset=utf-8',
        })

    def call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        xml_params: dict[str, str] | None = None,
    ) -> ET.Element:
        """Invoke a SOAP method and return the parsed response body.

        Args:
            method: The SOAP action / method name.
            params: Simple key-value parameters (string, int, etc.).
            xml_params: Parameters whose values are raw XML strings.

        Returns:
            The response ET.Element extracted from the SOAP body.

        Raises:
            RSGeConnectionError: On network or HTTP errors.
        """
        body_xml = self._build_body(method, params, xml_params)
        envelope = _SOAP_ENVELOPE.format(body=body_xml)
        soap_action = f'{_NAMESPACE}{method}'

        try:
            response = self._session.post(
                self._base_url,
                data    = envelope.encode('utf-8'),
                headers = {'SOAPAction': soap_action},
                timeout = self._timeout,
            )

            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise RSGeConnectionError(
                f'Failed to connect to RS.ge service: {exc}'
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise RSGeConnectionError(
                f'Request to RS.ge timed out after {self._timeout}s'
            ) from exc
        except requests.exceptions.HTTPError as exc:
            raise RSGeConnectionError(
                f'HTTP error from RS.ge: {exc.response.status_code}'
            ) from exc

        return self._parse_response(response.text, method)

    def _build_body(
        self,
        method: str,
        params: dict[str, Any] | None,
        xml_params: dict[str, str] | None,
    ) -> str:
        """Build the SOAP body XML for a given method call."""
        parts: list[str] = [f'<{method} xmlns="{_NAMESPACE}">']

        if params:
            for key, value in params.items():
                if value is None:
                    parts.append(f'<{key}/>')
                else:
                    escaped = (
                        str(value)
                        .replace('&', '&amp;')
                        .replace('<', '&lt;')
                        .replace('>', '&gt;')
                    )
                    parts.append(f'<{key}>{escaped}</{key}>')

        if xml_params:
            for key, xml_value in xml_params.items():
                parts.append(f'<{key}>{xml_value}</{key}>')

        parts.append(f'</{method}>')
        return '\n'.join(parts)

    def _parse_response(self, response_text: str, method: str) -> ET.Element:
        """Parse the SOAP response and extract the method result element."""
        if response_text.startswith('\ufeff'):
            response_text = response_text[1:]

        root = ET.fromstring(response_text)

        ns = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'rs': _NAMESPACE,
        }

        body = root.find('.//soap:Body', ns)
        if body is None:
            body = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')

        if body is None:
            raise RSGeConnectionError('Invalid SOAP response: missing Body element')

        result_tag = f'{method}Response'
        result_elem = None

        for child in body:
            tag = child.tag
            if '}' in tag:
                tag = tag.split('}')[1]
            if tag == result_tag:
                result_elem = child
                break

        if result_elem is None:
            return body

        for child in result_elem:
            tag = child.tag
            if '}' in tag:
                tag = tag.split('}')[1]
            if tag == f'{method}Result':
                return child

        return result_elem

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> SOAPTransport:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
