"""Invoice reference data: org info, units, barcodes, excise, declarations.

Demonstrates looking up organization info, measurement units,
barcode catalog management, excise products, and declaration operations.
"""

from rsge import InvoiceClient


def main():
    with InvoiceClient() as client:
        client.authenticate('your_username', 'your_password')

        # Look up organization info
        org = client.get_org_info('206322102')
        print(f'Organization: {org.name}')
        print(f'  TIN: {org.tin}')
        print(f'  Address: {org.address}')
        print(f'  VAT payer: {org.is_vat_payer}')
        print(f'  Diplomat: {org.is_diplomat}')

        # Check VAT payer status
        is_vat = client.get_vat_payer_status('206322102')
        print(f'\nVAT payer status: {is_vat}')

        # Get measurement units
        units = client.get_units()
        print(f'\nMeasurement units: {len(units)}')
        for u in units:
            print(f'  {u.value}: {u.label}')

        # List barcode catalog
        barcodes = client.list_bar_codes(maximum_rows=5)
        print(f'\nBarcode catalog: {len(barcodes)} entries')
        for bc in barcodes:
            print(f'  {bc.barcode}: {bc.goods_name} @ {bc.unit_price}')

        # Look up a specific barcode
        # bc = client.get_bar_code('0001')
        # print(f'Barcode 0001: {bc.goods_name}')

        # List excise products
        excise = client.list_excise(maximum_rows=5)
        print(f'\nExcise products: {len(excise)} entries')
        for item in excise:
            print(f'  {item}')

        # Declaration sequence number
        seq = client.get_seq_num(2025)
        print(f'\nDeclaration sequence (2025): {seq}')

        seq_monthly = client.get_seq_num(2025, 4)
        print(f'Declaration sequence (2025/04): {seq_monthly}')

        # Attach invoices to a declaration (uncomment to use)
        # client.create_decl([7624, 7625], year=2025, month=4)

        client.sign_out()


if __name__ == '__main__':
    main()
