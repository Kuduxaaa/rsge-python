"""
Manage personal barcode and vehicle catalogs.

Demonstrates registering, listing, and deleting barcodes
and vehicle numbers in the RS.ge service.
"""

from rsge import WayBillClient


def main():
    with WayBillClient('tbilisi', '123456') as client:
        client.save_bar_code('4860001000001', 'შაქარი 1კგ', unit_id=2)
        client.save_bar_code('4860001000002', 'ფქვილი 1კგ', unit_id=2)

        codes = client.get_bar_codes()
        print(f'Barcodes: {len(codes)}')
        for c in codes:
            print(f"  {c['bar_code']}: {c['goods_name']}")

        client.save_car_number('AA123BB')
        client.save_car_number('CC456DD')

        cars = client.get_car_numbers()
        print(f'\nVehicles: {cars}')

        client.delete_bar_code('4860001000002')
        client.delete_car_number('CC456DD')


if __name__ == '__main__':
    main()
