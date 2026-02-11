# Documentation

Complete reference documentation for the RS.ge Python SDK.

## Guides

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | Installation, requirements, quickstart examples for all three clients |
| [Exceptions](exceptions.md) | Exception hierarchy and error handling patterns |

## API Reference

| Document | Description |
|----------|-------------|
| [WayBill Client](waybill-client.md) | `WayBillClient` — SOAP/XML API for electronic commodity waybills (40+ methods) |
| [Customs Client](customs-client.md) | `CustomsClient` — REST/JSON API for customs declaration data |
| [Invoice Client](invoice-client.md) | `InvoiceClient` — REST/JSON API for tax invoices and declarations (25+ methods) |

## Data Reference

| Document | Description |
|----------|-------------|
| [Models](models.md) | All dataclass models — WayBill, Customs, and Invoice models with field tables |
| [Enums](enums.md) | All `IntEnum` types — waybill types/statuses, invoice categories/types, VAT types |

## API Overview

| Client | Protocol | Base URL | Auth |
|--------|----------|----------|------|
| `WayBillClient` | SOAP/XML | `https://services.rs.ge` | Service user + password |
| `CustomsClient` | REST/JSON | `https://services.rs.ge` | OAuth2 bearer token |
| `InvoiceClient` | REST/JSON | `https://eapi.rs.ge` | OAuth2 bearer token (with optional 2FA) |
