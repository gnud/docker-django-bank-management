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

    @staticmethod
    def test_create_userdata_success():
        """Raises ValidationError when non alphanumeric chars in iban's field"""
        UserdataFactory.create()


class UserdataAdminTest(TestCase):
    """Admin object based permissions access tests"""

    @classmethod
    def setUpTestData(cls):
        # Create admin user from different source
        cls.bob_credentials = ['admin_bob', 'admin_bob@example.com', "7u35ITpAss"]
        cls.root_credentials = ['admin_root', 'admin_root@example.com', "7u35ITpAss"]
        cls.create_admins()

        # Login the users
        cls.c_admin_root = cls.login_client(cls.root_credentials)
        cls.c_admin_bob = cls.login_client(cls.bob_credentials)

        # Create records
        Userdata.objects.create(owner=cls.user_bob, first_name='Alice', last_name='Doe', iban=make_iban(ISPB['BERLINER NOTSPA-RKA-SSE'], '12345', '123456'))
        Userdata.objects.create(owner=cls.user_root, first_name='Bob', last_name='Bob', iban=make_iban(ISPB['BERLINER NOTSPA-RKA-SSE'], '12345', '123456'))

    @classmethod
    def login_client(cls, credentials):
        client = Client()
        login = client.login(username=credentials[0], password=credentials[2])

        cls.assertTrue(cls, expr=login)

        return client

    @classmethod
    def create_admins(cls):
        cls.user_bob = get_user_model().objects.create_superuser(*cls.bob_credentials)
        cls.user_root = get_user_model().objects.create_superuser(*cls.root_credentials)

    def test_login_access(self):

        model_path = reverse('admin:banking_userdata_changelist')

        response1 = self.c_admin_root.get(model_path)
        response2 = self.c_admin_bob.get(model_path)

        # Test whether we can load the index of the admin
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_whether_bob_can_access_own_record(self):
        record_from_bob = Userdata.objects.filter(owner=self.user_bob).first()

        self.access_user_record(self.c_admin_bob, record_from_bob, 200)

    def test_whether_bob_can_access_root_record(self):
        record_from_root = Userdata.objects.filter(owner=self.user_root).first()

        self.access_user_record(self.c_admin_bob, record_from_root, 302)

    def access_user_record(self, c, record_from_root, expect):
        admin_url = reverse('admin:banking_userdata_change', args=[record_from_root.pk])
        response1 = c.get(admin_url)
        self.assertEqual(first=response1.status_code, second=expect, msg="ff")
