"""
Core exception classes for the RS.ge SDK.

All exceptions raised by the SDK inherit from RSGeError,
making it easy to catch any SDK-specific error in a single handler.
"""


class RSGeError(Exception):
    """
    Base exception for all RS.ge SDK errors.

    Attributes:
        message: Human-readable error description.
        code: Optional numeric error code from the RS.ge API.
    """

    def __init__(self, message: str, code: int | None = None) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class RSGeAuthenticationError(RSGeError):
    """
    Raised when authentication with the RS.ge service fails.
    """


class RSGeValidationError(RSGeError):
    """
    Raised when input data fails validation.
    """


class RSGeAPIError(RSGeError):
    """
    Raised when the RS.ge API returns a business-logic error.
    """


class RSGeConnectionError(RSGeError):
    """
    Raised when the SDK cannot reach the RS.ge servers.
    """


class RSGePermissionError(RSGeError):
    """
    Raised when the user lacks permission for the requested operation.
    """
