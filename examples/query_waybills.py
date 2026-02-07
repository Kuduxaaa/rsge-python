"""Query waybills from both seller and buyer perspectives.

Demonstrates listing waybills with filters and retrieving
full waybill details by ID.
"""

from rsge import WayBillClient, WayBillType


def main():
    with WayBillClient('tbilisi', '123456') as client:
        waybills = client.get_waybills(
            statuses      = ',1,',
            create_date_s = '2024-01-01',
            create_date_e = '2024-01-31',
        )

        print(f'Seller waybills: {len(waybills)}')
        for wb in waybills[:5]:
            print(f'  #{wb.id} | {wb.waybill_number} | {wb.buyer_name} | {wb.full_amount} GEL')

        buyer_wbs = client.get_buyer_waybills(
            create_date_s = '2024-01-01',
            create_date_e = '2024-01-31',
        )

        print(f'Buyer waybills: {len(buyer_wbs)}')

        if waybills:
            full = client.get_waybill(waybills[0].id)
            print(f'\nWaybill #{full.id} details:')
            print(f'  Type: {WayBillType(full.waybill_type).name}')
            print(f'  From: {full.start_address}')
            print(f'  To:   {full.end_address}')
            for g in full.goods_list:
                print(f'  - {g.name}: {g.quantity} x {g.price} = {g.amount}')


if __name__ == '__main__':
    main()
