import string

from django.core.exceptions import ValidationError
from django.test import TestCase
import factory
from .models import Userdata

ALPHA = {c: str(ord(c) % 55) for c in string.ascii_uppercase}

# noinspection SpellCheckingInspection
ISPB = {
    'BERLINER NOTSPA-RKA-SSE': 'BELADEBEXXX',
}


# noinspection SpellCheckingInspection
def make_iban(ispb, agency, account, country='BR', account_type='C', account_owner='1'):
    agency = agency.zfill(5)
    account = account.zfill(10)
    iban = ispb + agency + account + account_type + account_owner
    check = iban + country + '00'

    # import pdb; pdb.set_trace()
    check = int(''.join(ALPHA.get(c, c) for c in check))
    check = 98 - (check % 97)
    check = str(check).zfill(2)

    return country + check + iban


# noinspection SpellCheckingInspection
class UserdataFactory(factory.Factory):
    class Meta:
        model = Userdata

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    iban = make_iban(ISPB['BERLINER NOTSPA-RKA-SSE'], '12345', '123456')


# noinspection SpellCheckingInspection
class UserdataFactoryBad(factory.Factory):
    class Meta:
        model = Userdata

    first_name = 'Wrong Data$'
    last_name = factory.Faker('last_name')

    iban = str(make_iban(ISPB['BERLINER NOTSPA-RKA-SSE'], '12345', '123456'))
    iban = iban[0: -2] + "$"


# noinspection SpellCheckingInspection
class UserdataModelTest(TestCase):
    def test_string_representation(self):
        entry = Userdata(first_name="John", last_name="Doe")
        self.assertEqual(str(entry), "%s %s" % (entry.first_name, entry.last_name))

    def test_create_userdata_bad(self):
        """Raises ValidationError when non alphanumeric chars in iban's field"""
        userdata = UserdataFactoryBad.create()

        with self.assertRaises(ValidationError):
            userdata.full_clean()

    def test_create_userdata(self):
        """Raises ValidationError when non alphanumeric chars in iban's field"""
        userdata = UserdataFactory.create()
