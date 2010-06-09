from nose.tools import eq_

from robinhood.trident import TpgSale


class test_TpgSale():

    def test_success(self):

        data = {
                'card_number': '4012301230123010',
                'card_exp_date': '1111',
                'cardholder_street_address': '123 Main',
                'cardholder_zip': '55555',
                'invoice_number': '123',
                'transaction_amount': '1.25',
                'transaction_type': 'D',
                }

        r = TpgSale(data)

        eq_(r.execute(), True)

    def test_bad_card_number(self):

        data = {
                'card_number': '1234567890',
                'card_exp_date': '1111',
                'cardholder_street_address': '123 Main',
                'cardholder_zip': '55555',
                'invoice_number': '123',
                'transaction_amount': '1.25',
                'transaction_type': 'D',
                }

        r = TpgSale(data)

        eq_(r.execute(), False)
