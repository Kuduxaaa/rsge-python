"""Invoice management: list, query, confirm, refuse, cancel.

Demonstrates listing invoices with filters, querying details,
and performing buyer/seller lifecycle actions.
"""

from rsge import InvoiceClient, InvoiceListType


def main():
    with InvoiceClient() as client:
        client.authenticate('your_username', 'your_password')

        # List seller's own documents
        seller_docs = client.list_invoices(
            TYPE         = InvoiceListType.SELLER_DOCS,
            MAXIMUM_ROWS = 10,
        )
        print(f'Seller documents: {len(seller_docs)}')
        for inv in seller_docs:
            print(f'  #{inv.inv_number} | {inv.tin_buyer} | {inv.amount_full} GEL')

        # List buyer's received documents
        buyer_docs = client.list_invoices(
            TYPE         = InvoiceListType.BUYER_DOCS,
            MAXIMUM_ROWS = 10,
        )
        print(f'\nBuyer documents: {len(buyer_docs)}')
        for inv in buyer_docs:
            print(f'  #{inv.inv_number} | {inv.tin_seller} | {inv.amount_full} GEL')

        # Get full details for a specific invoice
        if seller_docs:
            detail = client.get_invoice(invoice_id=seller_docs[0].id)
            print(f'\nInvoice detail: #{detail.inv_number}')
            print(f'  Seller: {detail.tin_seller} ({detail.name_seller})')
            print(f'  Buyer:  {detail.tin_buyer} ({detail.name_buyer})')
            print(f'  Amount: {detail.amount_full} GEL (VAT: {detail.amount_vat})')
            print(f'  Goods:  {len(detail.invoice_goods)} items')

        # Confirm a buyer invoice (uncomment to use)
        # client.confirm_invoice(invoice_id=7624)

        # Refuse a buyer invoice (uncomment to use)
        # client.refuse_invoice(invoice_id=7624)

        # Cancel a seller invoice (uncomment to use)
        # client.cancel_invoice(invoice_id=7624)

        # Bulk operations (uncomment to use)
        # client.activate_invoices([7624, 7625, 7626])
        # client.confirm_invoices([7627, 7628])

        # Get available actions/statuses
        actions = client.get_actions()
        print(f'\nAvailable actions: {len(actions)}')
        for a in actions:
            print(f'  {a.id}: {a.name}')

        client.sign_out()


if __name__ == '__main__':
    main()
