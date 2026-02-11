"""Basic invoice workflow: authenticate, create, save, activate.

Demonstrates the full lifecycle of a tax invoice using the RS.ge
eAPI Invoice/Declaration service, including two-factor authentication.
"""

from rsge import (
    Invoice,
    InvoiceCategory,
    InvoiceClient,
    InvoiceType,
    InvoiceVATType,
)


def main():
    with InvoiceClient() as client:
        # Step 1: Authenticate (handles both 1FA and 2FA)
        auth = client.authenticate('satesto2', '123456')

        if auth.needs_pin:
            pin = input(f'Enter PIN sent to {auth.masked_mobile}: ')
            auth = client.authenticate_pin(auth.pin_token, pin)

        print(f'Authenticated (token: {auth.access_token[:20]}...)')

        # Step 2: Create an invoice
        # Note: sandbox only allows test TINs 206322102 and 12345678910
        inv = Invoice(
            inv_category        = InvoiceCategory.GOODS_SERVICE,
            inv_type            = InvoiceType.WITH_TRANSPORT,
            operation_date      = '10-02-2025 10:00:00',
            tin_seller          = '12345678910',
            tin_buyer           = '206322102',
            trans_start_address = 'თბილისი, რუსთაველის გამზ. 12',
            trans_end_address   = 'რუსთავი, მშვიდობის ქ. 5',
            trans_type          = 1,
            trans_car_no        = 'AB-123-CD',
            trans_driver_tin    = '206322102',
            trans_cost_payer    = 2,
        )

        # Step 3: Add goods (amount auto-calculated)
        inv.add_goods(
            goods_name = 'მაცივარი',
            quantity   = 2,
            unit_price = 900.0,
            unit_id    = 1,
            barcode    = '0001',
            vat_type   = InvoiceVATType.STANDARD,
        )

        inv.add_goods(
            goods_name = 'ტელევიზორი',
            quantity   = 1,
            unit_price = 1500.0,
            unit_id    = 1,
            barcode    = '0002',
        )

        print(f'Goods: {len(inv.invoice_goods)} items')
        for item in inv.invoice_goods:
            print(f'  {item.goods_name}: {item.quantity} x {item.unit_price} = {item.amount}')

        # Step 4: Save the invoice (async)
        txn_id = client.save_invoice(inv)
        print(f'Save submitted (transaction: {txn_id})')

        # Step 5: Poll for the result
        result = client.get_transaction_result(txn_id)
        print(f'Saved — Invoice ID: {result.invoice_id}')

        # Step 6: Activate
        saved_inv = client.get_invoice(invoice_id=result.invoice_id)
        client.activate_invoice(saved_inv)
        print(f'Activated invoice {result.invoice_id}')

        client.sign_out()
        print('Signed out')


if __name__ == '__main__':
    main()
