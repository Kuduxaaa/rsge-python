"""
Fetch reference/lookup data from the RS.ge API.

Demonstrates retrieving measurement units, transport types,
and looking up taxpayer names by TIN.
"""

from rsge import WayBillClient


def main():
    with WayBillClient('tbilisi', '123456') as client:
        units = client.get_waybill_units()
        print('Measurement units:')
        for u in units[:10]:
            print(f'  {u.id}: {u.name}')

        trans = client.get_transport_types()
        print('\nTransport types:')
        for t in trans:
            print(f'  {t.id}: {t.name}')

        name = client.get_name_from_tin('206322102')
        print(f'\nTIN 206322102 -> {name}')


if __name__ == '__main__':
    main()
