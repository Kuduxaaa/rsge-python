"""Tests for invoice model serialization and helpers."""

from rsge.invoice.models import (
    BarCode,
    Invoice,
    InvoiceAction,
    InvoiceAdvance,
    InvoiceAuthResponse,
    InvoiceGoods,
    InvoiceReturn,
    OrgInfo,
    SubInvoiceDistribution,
    TransactionResult,
    Unit,
)


class TestInvoiceAuthResponse:
    """Tests for InvoiceAuthResponse."""

    def test_needs_pin_true(self):
        resp = InvoiceAuthResponse(pin_token='abc123', access_token='')
        assert resp.needs_pin is True

    def test_needs_pin_false_with_token(self):
        resp = InvoiceAuthResponse(pin_token='abc', access_token='tok')
        assert resp.needs_pin is False

    def test_needs_pin_false_no_pin(self):
        resp = InvoiceAuthResponse(pin_token='', access_token='tok')
        assert resp.needs_pin is False

    def test_from_dict_one_factor(self):
        data = {
            'DATA': {
                'ACCESS_TOKEN': 'mytoken',
                'EXPIRES_IN': 2400,
                'MASKED_MOBILE': '*** *** *16',
            },
            'STATUS': {'ID': 0, 'TEXT': 'ok'},
        }
        resp = InvoiceAuthResponse.from_dict(data)
        assert resp.access_token == 'mytoken'
        assert resp.expires_in == 2400
        assert resp.needs_pin is False

    def test_from_dict_two_factor(self):
        data = {
            'DATA': {
                'PIN_TOKEN': 'pintoken123',
                'MASKED_MOBILE': '*** *** *28',
            },
            'STATUS': {'ID': 0, 'TEXT': 'ok'},
        }
        resp = InvoiceAuthResponse.from_dict(data)
        assert resp.pin_token == 'pintoken123'
        assert resp.access_token == ''
        assert resp.needs_pin is True


class TestInvoiceGoods:
    """Tests for InvoiceGoods round-trip."""

    def test_round_trip(self):
        original = InvoiceGoods(
            id=0,
            invoice_id=0,
            goods_name='მაცივარი',
            barcode='0001',
            unit_id=1,
            unit_txt='ცალი',
            quantity=2.0,
            unit_price=900.0,
            amount=1800.0,
            vat_amount=274.58,
            vat_type=0,
            excise_amount=0.0,
            excise_id=0,
            excise_unit_price=0.0,
        )
        d = original.to_dict()
        restored = InvoiceGoods.from_dict(d)
        assert restored.goods_name == 'მაცივარი'
        assert restored.quantity == 2.0
        assert restored.unit_price == 900.0
        assert restored.amount == 1800.0

    def test_from_dict_with_nulls(self):
        data = {
            'ID': 100,
            'INVOICE_ID': 50,
            'GOODS_NAME': 'Test',
            'QUANTITY': None,
            'UNIT_PRICE': None,
            'AMOUNT': None,
            'QUANTITY_EXT': None,
        }
        goods = InvoiceGoods.from_dict(data)
        assert goods.quantity == 0
        assert goods.unit_price == 0
        assert goods.quantity_ext == ''


class TestInvoiceReturn:
    """Tests for InvoiceReturn round-trip."""

    def test_to_dict(self):
        ret = InvoiceReturn(return_invoice_id=1103)
        d = ret.to_dict()
        assert d == {'RETURN_INVOICE_ID': 1103}

    def test_from_dict(self):
        data = {
            'RETURN_INVOICE_ID': 1103,
            'CORRECTED_INVOICE_ID': 999,
            'INV_NUMBER': '123',
        }
        ret = InvoiceReturn.from_dict(data)
        assert ret.return_invoice_id == 1103
        assert ret.corrected_invoice_id == 999


class TestInvoiceAdvance:
    """Tests for InvoiceAdvance."""

    def test_round_trip(self):
        adv = InvoiceAdvance(id=758, amount=1.0, operation_date='21-02-2019 16:19:30')
        d = adv.to_dict()
        assert d['ID'] == 758
        assert d['AMOUNT'] == 1.0
        assert d['OPERATION_DATE'] == '21-02-2019 16:19:30'

        restored = InvoiceAdvance.from_dict(d)
        assert restored.id == 758
        assert restored.amount == 1.0


class TestSubInvoiceDistribution:
    """Tests for SubInvoiceDistribution."""

    def test_from_dict(self):
        data = {
            'PARENT_INVOICE_ID': 100,
            'SUB_INVOICE_ID': 200,
            'INV_NUMBER': '456',
            'AMOUNT_FULL': 5000.0,
        }
        sub = SubInvoiceDistribution.from_dict(data)
        assert sub.parent_invoice_id == 100
        assert sub.sub_invoice_id == 200
        assert sub.amount_full == 5000.0


class TestInvoice:
    """Tests for Invoice model."""

    def test_add_goods_calculates_amount(self):
        inv = Invoice()
        item = inv.add_goods('Test Product', quantity=3.0, unit_price=100.0)
        assert item.amount == 300.0
        assert len(inv.invoice_goods) == 1
        assert inv.invoice_goods[0].goods_name == 'Test Product'

    def test_round_trip(self):
        inv = Invoice(
            id=0,
            inv_category=1,
            inv_type=2,
            operation_date='10-04-2019 10:00:00',
            tin_seller='206322102',
            tin_buyer='12345678910',
            amount_full=3750,
            trans_start_address='თბილისი',
            trans_end_address='რუსთავი',
        )
        inv.add_goods('მაცივარი', quantity=2.0, unit_price=900.0, barcode='0001')

        d = inv.to_dict()
        assert d['INV_CATEGORY'] == 1
        assert d['TIN_SELLER'] == '206322102'
        assert len(d['INVOICE_GOODS']) == 1
        assert d['INVOICE_GOODS'][0]['GOODS_NAME'] == 'მაცივარი'

        restored = Invoice.from_dict(d)
        assert restored.inv_category == 1
        assert restored.tin_seller == '206322102'
        assert len(restored.invoice_goods) == 1

    def test_from_dict_full_response(self):
        """Test parsing a full GetInvoice response."""
        data = {
            'ID': 7624,
            'INV_SERIE': '',
            'INV_NUMBER': '19095',
            'INV_CATEGORY': 1,
            'INV_TYPE': 2,
            'SELLER_ACTION': 0,
            'BUYER_ACTION': 0,
            'OPERATION_DATE': '10-04-2019 00:00:00',
            'ACTIVATE_DATE': '',
            'CREATE_DATE': '13-04-2019 13:36:25',
            'TIN_SELLER': '206322102',
            'TIN_BUYER': '12345678910',
            'FOREIGN_BUYER': 'false',
            'AMOUNT_FULL': 3750,
            'AMOUNT_VAT': 572.03,
            'INVOICE_GOODS': [
                {
                    'ID': 18568,
                    'INVOICE_ID': 7624,
                    'GOODS_NAME': 'მაცივარი',
                    'BARCODE': '0001',
                    'UNIT_ID': 1,
                    'QUANTITY': 2.0,
                    'UNIT_PRICE': 900.0,
                    'AMOUNT': 1800.0,
                    'VAT_AMOUNT': 274.58,
                    'VAT_TYPE': 0,
                },
            ],
            'INVOICE_RETURN': [],
            'SUB_INVOICES_DISTRIBUTION': [],
            'INVOICE_ADVANCE': [
                {
                    'PARENT_INVOICE_ID': 7624,
                    'ID': 5954,
                    'AMOUNT': 1.0,
                    'OPERATION_DATE': '25-12-2018 13:36:25',
                },
            ],
            'INVOICE_OIL_DOCS': [],
        }
        inv = Invoice.from_dict(data)
        assert inv.id == 7624
        assert inv.inv_number == '19095'
        assert len(inv.invoice_goods) == 1
        assert inv.invoice_goods[0].goods_name == 'მაცივარი'
        assert len(inv.invoice_advance) == 1
        assert inv.invoice_advance[0].amount == 1.0


class TestInvoiceAction:
    """Tests for InvoiceAction."""

    def test_from_dict(self):
        data = {'ID': '3', 'NAME': 'აქტიური', 'SELLER_ACTION': '1', 'BUYER_ACTION': '0'}
        action = InvoiceAction.from_dict(data)
        assert action.id == 3
        assert action.name == 'აქტიური'
        assert action.seller_action == 1


class TestUnit:
    """Tests for Unit."""

    def test_from_dict(self):
        data = {'value': '1', 'label': 'ცალი'}
        unit = Unit.from_dict(data)
        assert unit.value == '1'
        assert unit.label == 'ცალი'


class TestOrgInfo:
    """Tests for OrgInfo."""

    def test_from_dict(self):
        data = {
            'Tin': '206322102',
            'Address': 'ოზურგეთის რაიონი / შაუმიანის ',
            'IsVatPayer': True,
            'IsDiplomat': False,
            'Name': 'სატესტო კოდი1',
        }
        org = OrgInfo.from_dict(data)
        assert org.tin == '206322102'
        assert org.is_vat_payer is True
        assert org.is_diplomat is False
        assert org.name == 'სატესტო კოდი1'


class TestBarCode:
    """Tests for BarCode."""

    def test_from_dict(self):
        data = {
            'BARCODE': '55',
            'GOODS_NAME': 'xaxvi',
            'UNIT_ID': '2',
            'UNIT_TXT': 'კგ',
            'VAT_TYPE': '0',
            'UNIT_PRICE': '1',
        }
        bc = BarCode.from_dict(data)
        assert bc.barcode == '55'
        assert bc.goods_name == 'xaxvi'
        assert bc.unit_price == 1.0


class TestTransactionResult:
    """Tests for TransactionResult."""

    def test_from_dict(self):
        data = {'INVOICE_ID': '913'}
        tr = TransactionResult.from_dict(data)
        assert tr.invoice_id == 913
