"""Basic waybill workflow: create, add goods, save, activate, and close.

Demonstrates the full lifecycle of an electronic commodity waybill
using the RS.ge WayBill SOAP service.
"""

from rsge import (
    TransportCostPayer,
    VATType,
    WayBillClient,
    WayBillType,
)


def main():
    with WayBillClient('tbilisi', '123456') as client:
        un_id, user_id = client.check_service_user()
        print(f'Authenticated — TIN: {un_id}, User ID: {user_id}')

        wb = client.create_waybill(
            waybill_type         = WayBillType.TRANSPORTATION,
            buyer_tin            = '12345678910',
            buyer_name           = 'შპს ტესტი',
            start_address        = 'თბილისი, რუსთაველის გამზ. 12',
            end_address          = 'ბათუმი, გორგილაძის ქ. 5',
            driver_tin           = '01234567890',
            driver_name          = 'გიორგი გიორგაძე',
            car_number           = 'AA123BB',
            transport_cost_payer = TransportCostPayer.SELLER,
            comment              = 'სატესტო ზედნადები',
        )

        wb.add_goods(
            name     = 'შაქარი',
            unit_id  = 2,
            quantity = 500,
            price    = 2.50,
            bar_code = '4860001000001',
            vat_type = VATType.REGULAR,
        )

        wb.add_goods(
            name     = 'ფქვილი',
            unit_id  = 2,
            quantity = 300,
            price    = 1.80,
            bar_code = '4860001000002',
            vat_type = VATType.REGULAR,
        )

        print(f'Goods: {len(wb.goods_list)} items, total: {wb.full_amount} GEL')

        result = client.save_waybill(wb)
        if result.is_success:
            print(f'Saved — Waybill ID: {result.waybill_id}')

            wb_number = client.activate_waybill(result.waybill_id)
            print(f'Activated — Number: {wb_number}')

            client.close_waybill(result.waybill_id)
            print('Closed — Delivery complete')
        else:
            print(f'Save failed: code {result.status}')


if __name__ == '__main__':
    main()
