# Exceptions Reference

All exceptions raised by the SDK inherit from `RSGeError`, making it easy to catch any SDK-specific error in a single handler. Import them directly from `rsge`:

```python
from rsge import (
    RSGeError,
    RSGeAuthenticationError,
    RSGeValidationError,
    RSGeAPIError,
    RSGeConnectionError,
)
```

**Source:** `rsge/core/exceptions.py`

---

## Exception Hierarchy

```
Exception
└── RSGeError
    ├── RSGeAuthenticationError
    ├── RSGeValidationError
    ├── RSGeAPIError
    ├── RSGeConnectionError
    └── RSGePermissionError
```

---

## Base Exception

### `RSGeError`

Base exception for all RS.ge SDK errors.

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Human-readable error description |
| `code` | `int \| None` | Optional numeric error code from the RS.ge API |

```python
try:
    result = client.save_waybill(waybill)
except RSGeError as exc:
    print(f'Error: {exc.message}')
    if exc.code is not None:
        print(f'Code: {exc.code}')
```

---

## Specific Exceptions

### `RSGeAuthenticationError`

Raised when authentication with the RS.ge service fails. Common causes:

- Invalid service username or password
- Expired or missing credentials
- Customs API called without authenticating first

```python
try:
    client.check_service_user()
except RSGeAuthenticationError:
    print('Invalid credentials')
```

Known error codes:
- `-100` — Invalid service credentials

### `RSGeValidationError`

Raised when input data fails validation before being sent to the API.

### `RSGeAPIError`

Raised when the RS.ge API returns a business-logic error (negative error codes). This is the most common error type during normal operations.

```python
try:
    client.close_waybill(waybill_id)
except RSGeAPIError as exc:
    print(f'API error {exc.code}: {exc.message}')
```

### `RSGeConnectionError`

Raised when the SDK cannot reach the RS.ge servers. Common causes:

- Network connectivity issues
- DNS resolution failure
- RS.ge service downtime

```python
try:
    client.check_service_user()
except RSGeConnectionError:
    print('Cannot reach RS.ge servers')
```

### `RSGePermissionError`

Raised when the user lacks permission for the requested operation.

Known error codes:
- `-101` — Cannot modify another user's waybill

---

## Error Handling Patterns

### Catch all SDK errors

```python
from rsge import RSGeError

try:
    result = client.save_waybill(waybill)
except RSGeError as exc:
    print(f'SDK error: {exc.message}')
```

### Handle specific errors

```python
from rsge import (
    RSGeAuthenticationError,
    RSGeAPIError,
    RSGeConnectionError,
)

try:
    client.check_service_user()
    result = client.save_waybill(waybill)
    client.activate_waybill(result.waybill_id)
except RSGeAuthenticationError:
    print('Check your credentials')
except RSGeConnectionError:
    print('Network error, retrying...')
except RSGeAPIError as exc:
    print(f'Business error {exc.code}: {exc.message}')
```

### Look up error codes programmatically

The RS.ge API provides a list of all error codes and descriptions:

```python
error_codes = client.get_error_codes()
for ec in error_codes:
    print(f'{ec.id}: {ec.text} (type={ec.error_type})')
```

Error types: `1` = waybill error, `2` = goods item error, `3` = invoice error.
