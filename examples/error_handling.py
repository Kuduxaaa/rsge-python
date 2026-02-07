"""Error handling patterns for the RS.ge SDK.

Demonstrates catching authentication errors, API errors,
and unexpected exceptions when using the SDK.
"""

from rsge import (
    RSGeAPIError,
    RSGeAuthenticationError,
    WayBillClient,
)


def main():
    try:
        client = WayBillClient('wrong_user', 'wrong_pass')
        client.check_service_user()

    except RSGeAuthenticationError as e:
        print(f'Auth failed: {e}')

    except RSGeAPIError as e:
        print(f'API error (code {e.code}): {e}')

    except Exception as e:
        print(f'Unexpected error: {e}')


if __name__ == '__main__':
    main()
