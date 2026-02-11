"""Monthly declaration for მცირე მეწარმე (small business, 1% tax).

Demonstrates listing invoices eligible for declaration binding,
checking the sequence number, and creating a monthly declaration.

Note: create_decl() may fail on sandbox because test invoices
don't meet the attachment conditions required for declarations.
"""

from rsge import InvoiceClient, InvoiceListType
from rsge.core.exceptions import RSGeAPIError


def main():
    with InvoiceClient() as client:
        auth = client.authenticate('satesto2', '123456')

        if auth.needs_pin:
            pin = input(f'Enter PIN sent to {auth.masked_mobile}: ')
            auth = client.authenticate_pin(auth.pin_token, pin)

        print(f'Authenticated (token: {auth.access_token[:20]}...)')

        year, month = 2025, 2

        # Step 1: List seller invoices eligible for declaration
        invoices = client.list_invoices(TYPE=InvoiceListType.SELLER_DECL)

        print(f'\nInvoices eligible for declaration: {len(invoices)}')
        for inv in invoices:
            print(f'  #{inv.id} | {inv.inv_number} | {inv.amount_full} GEL')

        if not invoices:
            print('No invoices to attach — nothing to declare')
            client.sign_out()
            return

        # Step 2: Check sequence number
        seq = client.get_seq_num(year, month)
        print(f'\nSequence number ({year}/{month:02d}): {seq}')

        # Step 3: Create monthly declaration with all eligible invoices
        invoice_ids = [inv.id for inv in invoices]
        try:
            client.create_decl(invoice_ids, year=year, month=month)
            print(f'Declaration created — {len(invoice_ids)} invoice(s) attached to {year}/{month:02d}')
        except RSGeAPIError as exc:
            print(f'Note: create_decl() not available on sandbox: {exc}')

        client.sign_out()
        print('Signed out')


if __name__ == '__main__':
    main()
