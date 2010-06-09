import urllib
import urlparse

try:
    from manage import settings
except:
    from django.conf import settings


class TpgTransaction:
    """Read the "Mes Gateway Specifications" file linked to at this address:
        http://resources.merchante-solutions.com/display/TPGPUB/MeS+Payment+Gateway+Developer%27s+Guide
    """

    request_fields = {
            'card_number': None,
            'card_exp_date': None,
            'cardholder_street_address': None,
            'cardholder_zip': None,
            'invoice_number': None,

            'transaction_amount': None,

            # D=Sale, V=Void, U=Refund, G=Forex (undocumented!)
            'transaction_type': None,
        }

    def __init__(self, data, *args, **kwargs):

        for key in data:
            if key in self.request_fields:
                self.request_fields[key] = data[key]
            else:
                # Log invalid request field
                pass

    def execute(self):
        """Connects to the remote server and runs the transaction."""

        if not self.validate():
            # TODO
            pass

        #TODO Strip out empty fields
        f = self.request_fields

        f.update({'profile_id': settings.E_COMMERCE['profile_id'],
                  'profile_key': settings.E_COMMERCE['profile_key']})

        params = urllib.urlencode(f)
        r = urllib.urlopen("%s?%s" % (settings.E_COMMERCE['api_host'], params)).read()

        response = urlparse.parse_qs(r)

        if response['error_code'][0] == "000":
            return True
        else:
            return False


    def validate(self):
        """Local validation of data.  This should be used before executing the
        transaction."""
        #TODO
        return True


class TpgRefund(TpgTransaction):
    pass

class TpgSale(TpgTransaction):
    pass

class TpgVoid(TpgTransaction):
    pass


