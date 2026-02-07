# Customs Client API Reference

`rsge.CustomsClient` provides access to assessed customs declarations data from the RS.ge REST API, using OAuth2-style bearer token authentication.

## Constructor

```python
CustomsClient(
    base_url:   str  = 'https://services.rs.ge',
    timeout:    int  = 30,
    verify_ssl: bool = True,
)
```

| Parameter | Description |
|-----------|-------------|
| `base_url` | API base URL (override for testing) |
| `timeout` | HTTP request timeout in seconds |
| `verify_ssl` | Whether to verify SSL certificates |

Supports context manager protocol:

```python
with CustomsClient() as client:
    ...
```

---

## Authentication

The customs API supports two authentication flows:

### One-Factor Authentication

```python
from rsge import CustomsClient

with CustomsClient() as client:
    auth = client.authenticate('username', 'password')
    print(f'Authenticated: {auth.access_token[:20]}...')
```

### Two-Factor Authentication (PIN)

If the account has 2FA enabled, the first `authenticate()` call returns a response without an access token but with a `PIN_TOKEN`. The user receives a PIN code (e.g., via SMS), which must be submitted with `authenticate_pin()`:

```python
from rsge import CustomsClient

with CustomsClient() as client:
    auth = client.authenticate('username', 'password', device_code='my-app-001')

    if not auth.access_token:
        pin = input('Enter PIN: ')
        auth = client.authenticate_pin(
            pin_token   = auth.message,
            pin         = pin,
            device_code = 'my-app-001',
            save_device = True,
        )

    declarations = client.get_declarations('2024-01-01', '2024-01-31')
```

---

## Methods

### `authenticate(username, password, device_code='') -> CustomsAuthResponse`

Authenticate with the customs API (one-factor).

```python
def authenticate(
    self,
    username:    str,
    password:    str,
    device_code: str = '',
) -> CustomsAuthResponse
```

| Parameter | Description |
|-----------|-------------|
| `username` | Portal username |
| `password` | Portal password |
| `device_code` | Optional device identifier (for 2FA device saving) |

**Returns:** `CustomsAuthResponse` with `access_token`, `status`, and `message`.

**Raises:** `RSGeAuthenticationError` if credentials are invalid.

On success, the client automatically stores the access token and sets the `Authorization` header for subsequent requests.

### `authenticate_pin(pin_token, pin, device_code='', *, save_device=False, address='', browser='', oper_system='') -> CustomsAuthResponse`

Complete two-factor authentication with a PIN code.

```python
def authenticate_pin(
    self,
    pin_token:   str,
    pin:         str,
    device_code: str  = '',
    *,
    save_device: bool = False,
    address:     str  = '',
    browser:     str  = '',
    oper_system: str  = '',
) -> CustomsAuthResponse
```

| Parameter | Description |
|-----------|-------------|
| `pin_token` | Token from the first authentication step |
| `pin` | The PIN code sent to the user |
| `device_code` | Device identifier |
| `save_device` | Whether to remember this device (skip 2FA next time) |
| `address` | Client IP/address (for device saving) |
| `browser` | Browser identifier |
| `oper_system` | OS identifier |

### `get_declarations(date_from, date_to) -> list[CustomsDeclaration]`

Retrieve assessed customs declarations for a date range.

```python
declarations = client.get_declarations(
    date_from = '2024-01-01',
    date_to   = '2024-01-31',
)

for decl in declarations:
    print(f'{decl.declaration_number}: {decl.commodity_code}')
    print(f'  Value: {decl.customs_value}, Duty: {decl.duty_amount}')
```

| Parameter | Description |
|-----------|-------------|
| `date_from` | Start date (ISO format, e.g., `'2024-01-01'`) |
| `date_to` | End date (ISO format) |

**Returns:** List of `CustomsDeclaration` objects.

**Raises:**
- `RSGeAuthenticationError` if not authenticated (call `authenticate()` first)
- `RSGeAPIError` on API errors

### `sign_out() -> bool`

Sign out and invalidate the current access token. Returns `True` on success.

```python
client.sign_out()
```

### `is_authenticated -> bool`

Property that checks whether an access token is currently set.

```python
if client.is_authenticated:
    declarations = client.get_declarations(...)
```

---

## Session Management

### `close() -> None`

Close the underlying HTTP session. Called automatically when using `with` statement.
