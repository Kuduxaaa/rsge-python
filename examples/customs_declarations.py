"""
Retrieve customs declarations via the REST API.

Demonstrates authenticating with the customs API,
fetching declarations by date range, and signing out.
"""

from rsge import CustomsClient


def main():
    with CustomsClient() as client:
        auth = client.authenticate('your_username', 'your_password')
        print(f'Authenticated (token: {auth.access_token[:20]}...)')

        declarations = client.get_declarations(
            date_from = '2024-01-01',
            date_to   = '2024-03-31',
        )

        print(f'Declarations: {len(declarations)}')

        for d in declarations:
            print(
                f'  {d.declaration_number} | '
                f'{d.commodity_code} | '
                f'{d.description[:40]} | '
                f'Value: {d.customs_value} | '
                f'Duty: {d.duty_amount}'
            )

        client.sign_out()
        print('Signed out')


if __name__ == '__main__':
    main()
