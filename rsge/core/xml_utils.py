"""XML helper utilities for building and parsing SOAP requests/responses.

The RS.ge WayBill service uses a SOAP/XML interface. This module provides
thin wrappers to simplify XML construction and extraction so that the
rest of the SDK can work with native Python objects.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any


def build_element(tag: str, text: str | None = None, **attribs: str) -> ET.Element:
    """Create an XML element with optional text content and attributes.

    Args:
        tag: The element tag name.
        text: Optional text content for the element.
        **attribs: Optional XML attributes.

    Returns:
        A new ET.Element instance.
    """
    elem = ET.Element(tag, dict(attribs))
    if text is not None:
        elem.text = str(text)
    return elem


def add_child(parent: ET.Element, tag: str, text: Any = None) -> ET.Element:
    """Append a child element to a parent.

    Args:
        parent: The parent element.
        tag: The child element tag name.
        text: Optional text content (will be converted to str).

    Returns:
        The newly created child element.
    """
    child = ET.SubElement(parent, tag)
    if text is not None:
        child.text = str(text)
    return child


def get_text(element: ET.Element, tag: str, default: str = '') -> str:
    """Extract text content from a child element.

    Args:
        element: The parent element to search within.
        tag: The child element tag name.
        default: Value to return if the child is missing or has no text.

    Returns:
        The text content, or default if not found.
    """
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return default


def get_int(element: ET.Element, tag: str, default: int = 0) -> int:
    """Extract an integer value from a child element.

    Args:
        element: The parent element to search within.
        tag: The child element tag name.
        default: Value to return if the child is missing or not numeric.

    Returns:
        The parsed integer, or default.
    """
    text = get_text(element, tag, '')
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        return default


def get_decimal(element: ET.Element, tag: str, default: float = 0.0) -> float:
    """Extract a decimal/float value from a child element.

    Args:
        element: The parent element to search within.
        tag: The child element tag name.
        default: Value to return if the child is missing or not numeric.

    Returns:
        The parsed float, or default.
    """
    text = get_text(element, tag, '')
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def element_to_string(element: ET.Element) -> str:
    """Serialize an XML element to a UTF-8 string.

    Args:
        element: The element to serialize.

    Returns:
        The XML string representation.
    """
    return ET.tostring(element, encoding='unicode')


def parse_xml_string(xml_string: str) -> ET.Element:
    """Parse an XML string into an element tree.

    Args:
        xml_string: The raw XML string.

    Returns:
        The root ET.Element.

    Raises:
        ET.ParseError: If the XML is malformed.
    """
    return ET.fromstring(xml_string)
