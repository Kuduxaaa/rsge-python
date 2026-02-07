"""
Waybill with transporter workflow.

Demonstrates the full flow: seller creates and forwards a waybill
to a transporter company, then the transporter activates and closes it.
"""

from datetime import datetime

from rsge import WayBillClient, WayBillType


def main():
    with WayBillClient('tbilisi', '123456') as seller:
        wb = seller.create_waybill(
            waybill_type    = WayBillType.TRANSPORTATION,
            buyer_tin       = '12345678910',
            buyer_name      = 'შპს მყიდველი',
            start_address   = 'თბილისი',
            end_address     = 'ქუთაისი',
            transporter_tin = '99999999999',
        )

        wb.add_goods(name='ტვირთი', unit_id=2, quantity=1000, price=5.0, bar_code='001')

        result = seller.save_waybill(wb)
        waybill_id = result.waybill_id
        print(f'Seller saved waybill: {waybill_id}')

        seller.activate_waybill(waybill_id)
        print('Sent to transporter')

    with WayBillClient('satesto2', '123456') as transporter:
        transporter.save_waybill_transporter(
            waybill_id  = waybill_id,
            car_number  = 'TT999GG',
            driver_tin  = '01234567890',
            driver_name = 'მძღოლი მძღოლაშვილი',
        )

        print('Transporter saved details')

        code, number = transporter.activate_waybill_transporter(
            waybill_id = waybill_id,
            begin_date = datetime.now(),
        )

        print(f'Transporter activated: {number}')

        transporter.close_waybill_transporter(
            waybill_id    = waybill_id,
            delivery_date = datetime.now(),
        )

        print('Transporter closed — delivery complete')


if __name__ == '__main__':
    main()
