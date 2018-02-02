import string

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
import factory
from django.urls import reverse

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

    def test_create_userdata_bad_iban(self):
        """Raises ValidationError when non alphanumeric chars in iban's field"""
        userdata = UserdataFactoryBad.create()

        with self.assertRaises(ValidationError):
            userdata.full_clean()

    def test_create_userdata_bad_first_name(self):
        """Raises ValidationError when non alphanumeric chars in first_name's field"""
        userdata = UserdataFactory.create(first_name=52 * "John ")

        with self.assertRaises(ValidationError):
            userdata.full_clean()

    def test_create_userdata_bad_last_name(self):
        """Raises ValidationError when non alphanumeric chars in last_name's field"""
        userdata = UserdataFactory.create(last_name=80 * " Doe")

        with self.assertRaises(ValidationError):
            userdata.full_clean()

    def test_create_userdata_success(self):
        """Raises ValidationError when non alphanumeric chars in iban's field"""
        UserdataFactory.create()


class UserdataAdminTest(TestCase):
    def test_access_owned_record(self):

        self.bob_credentials = ['admin_bob', 'admin_bob@example.com', "7u35ITpAss"]
        self.root_credentials = ['admin_root', 'admin_root@example.com', "7u35ITpAss"]
        self.create_admins()

        c_admin_root = self.login_client(self.root_credentials)
        c_admin_bob = self.login_client(self.bob_credentials)

        model_path = reverse('admin:banking_userdata_changelist')

        response1 = c_admin_root.get(model_path)
        response2 = c_admin_bob.get(model_path)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def login_client(self, credentials):
        client = Client()
        login = client.login(username=credentials[0], password=credentials[2])

        self.assertTrue(login)

        return client

    def create_admins(self):
        admin_bob = get_user_model().objects.create_superuser(*self.bob_credentials)
        admin_john = get_user_model().objects.create_superuser(*self.root_credentials)

    def test_access_others_record(self):
        pass
