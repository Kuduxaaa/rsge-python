"""Save and reuse waybill templates.

Demonstrates creating a waybill template, listing templates,
loading a template, and creating a waybill from it.
"""

from rsge import WayBillClient, WayBillType


def main():
    with WayBillClient('tbilisi', '123456') as client:
        wb = client.create_waybill(
            waybill_type  = WayBillType.TRANSPORTATION,
            buyer_tin     = '12345678910',
            buyer_name    = 'შპს მუდმივი მყიდველი',
            start_address = 'თბილისი, საწყობი',
            end_address   = 'ბათუმი, პორტი',
        )

        wb.add_goods(
            name     = 'სტანდარტული ტვირთი',
            unit_id  = 2,
            quantity = 100,
            price    = 10.0,
            bar_code = 'STD01',
        )

        client.save_waybill_template('ბათუმის მარშრუტი', wb)
        print('Template saved')

        templates = client.get_waybill_templates()
        for t in templates:
            print(f"  Template #{t['id']}: {t['name']}")

        if templates:
            loaded = client.get_waybill_template(templates[0]['id'])
            loaded.buyer_name = 'შპს ახალი მყიდველი'
            result = client.save_waybill(loaded)
            print(f'Waybill from template: {result.waybill_id}')


if __name__ == '__main__':
    main()
