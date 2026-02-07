"""
Distribution waybill with sub-waybills for multi-stop delivery.

Demonstrates creating a parent distribution waybill and attaching
child sub-waybills for partial deliveries to different buyers.
"""

from rsge import WayBillClient, WayBillType


def main():
    with WayBillClient('tbilisi', '123456') as client:
        main_wb = client.create_waybill(
            waybill_type  = WayBillType.DISTRIBUTION,
            start_address = 'თბილისი, საწყობი',
            end_address   = 'თბილისი',
            driver_tin    = '01234567890',
            driver_name   = 'მძღოლი',
            car_number    = 'DD111EE',
        )

        main_wb.add_goods(name='პროდუქცია A', unit_id=2, quantity=100, price=10.0, bar_code='A01')
        main_wb.add_goods(name='პროდუქცია B', unit_id=2, quantity=200, price=5.0, bar_code='B01')

        result = client.save_waybill(main_wb)
        parent_id = str(result.waybill_id)
        print(f'Main distribution waybill: {parent_id}')

        sub1 = client.create_waybill(
            waybill_type  = WayBillType.SUB_WAYBILL,
            buyer_tin     = '11111111111',
            buyer_name    = 'მაღაზია 1',
            start_address = 'თბილისი, საწყობი',
            end_address   = 'თბილისი, ვაჟა-ფშაველას 10',
            parent_id     = parent_id,
        )

        sub1.add_goods(name='პროდუქცია A', unit_id=2, quantity=40, price=10.0, bar_code='A01')

        result1 = client.save_waybill(sub1)
        print(f'Sub-waybill 1: {result1.waybill_id}')

        sub2 = client.create_waybill(
            waybill_type  = WayBillType.SUB_WAYBILL,
            buyer_tin     = '22222222222',
            buyer_name    = 'მაღაზია 2',
            start_address = 'თბილისი, საწყობი',
            end_address   = 'თბილისი, აღმაშენებლის 55',
            parent_id     = parent_id,
        )

        sub2.add_goods(name='პროდუქცია B', unit_id=2, quantity=100, price=5.0, bar_code='B01')

        result2 = client.save_waybill(sub2)
        print(f'Sub-waybill 2: {result2.waybill_id}')


if __name__ == '__main__':
    main()
