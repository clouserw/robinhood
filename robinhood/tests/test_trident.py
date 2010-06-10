from nose.tools import eq_
from xml.dom.minidom import parseString

from robinhood.trident import TpgCurrency, TpgSale


class test_TpgSale():

    def test_success(self):

        data = {
                'card_number': '4012301230123010',
                'card_exp_date': '1111',
                'cardholder_street_address': '123 Main',
                'cardholder_zip': '55555',
                'currency_code': '840',
                'invoice_number': '123',
                'transaction_amount': '1.25',
                'transaction_type': 'D',
                }

        r = TpgSale(data)

        eq_(r.execute()['error_code'][0], '000')

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

        eq_(r.execute()['error_code'][0], '117')  # Card type not accepted

class test_TpgCurrency():

    def test_success(self):

        data = {
                'currency_code': 978,  #EUR
                'transaction_type': 'G',
                }

        r = TpgCurrency(data)

        response = r.execute()

        eq_(response['error_code'][0], '000')

        d = parseString(response['fx_rate'][0])

        n = d.getElementsByTagName("MerchantCurrencyCode")[0].childNodes[0].data
        eq_(n, 'USD')
        p = d.getElementsByTagName("ConsumerCurrencyCode")[0].childNodes[0].data
        eq_(p, 'EUR')

        # Will throw an exception if it's not a valid float
        rate = float(d.getElementsByTagName("Rate")[0].childNodes[0].data)
