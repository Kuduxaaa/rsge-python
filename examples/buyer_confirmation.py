"""Buyer confirms or rejects received waybills.

Demonstrates querying unconfirmed waybills as a buyer
and confirming or rejecting them.
"""

from rsge import WayBillClient


def main():
    with WayBillClient('satesto2', '123456') as buyer:
        waybills = buyer.get_buyer_waybills_ex(
            statuses      = ',2,',
            is_confirmed  = 0,
            create_date_s = '2024-01-01',
            create_date_e = '2024-12-31',
        )

        print(f'Pending confirmation: {len(waybills)}')

        for wb in waybills:
            print(f'  #{wb.id} from {wb.seller_name}: {wb.full_amount} GEL')

            if wb.full_amount > 0:
                buyer.confirm_waybill(wb.id)
                print('    -> Confirmed')
            else:
                buyer.reject_waybill(wb.id)
                print('    -> Rejected')


if __name__ == '__main__':
    main()
