from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
import factory
from django.urls import reverse
from schwifty import IBAN

from .models import Userdata


class UserdataModelTest(TestCase):
    @classmethod
    def create_admins(cls):
        cls.user_bob = get_user_model().objects.create_superuser(*cls.bob_credentials)
        cls.user_root = get_user_model().objects.create_superuser(*cls.root_credentials)

    @classmethod
    def setUpTestData(cls):
        # Create admin user from different source
        cls.bob_credentials = ['admin_bob', 'admin_bob@example.com', "7u35ITpAss"]
        cls.root_credentials = ['admin_root', 'admin_root@example.com', "7u35ITpAss"]
        cls.create_admins()

    def test_create_userdata_good_iban(self):
        """iban's field passes"""

        first_name = factory.Faker('first_name').generate('')
        last_name = factory.Faker('last_name').generate('')

        iban = IBAN.generate(country_code='DE', bank_code='37040044', account_code='0532013000').formatted

        result = Userdata(first_name=first_name, last_name=last_name, iban=iban, owner=get_user_model().objects.first())
        result.full_clean()

        self.assertTrue(expr=result)

    def test_create_userdata_bad_iban(self):
        """Raises ValidationError when non alphanumeric chars in iban's field"""

        first_name = factory.Faker('first_name').generate('')
        last_name = factory.Faker('last_name').generate('')

        # iban = IBAN.generate(country_code='DE', bank_code='37040044', account_code='0532013000').formatted

        with self.assertRaises(ValidationError):
            Userdata(first_name=first_name, last_name=last_name, iban="fdfghfds", owner=get_user_model().objects.first()).full_clean()

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
        Userdata.objects.create(owner=cls.user_bob, first_name='Alice', last_name='Doe', iban=IBAN.generate(country_code='DE', bank_code='37040044', account_code='0532013000').formatted)
        Userdata.objects.create(owner=cls.user_root, first_name='Bob', last_name='Bob', iban=IBAN.generate(country_code='DE', bank_code='37040044', account_code='0532013000').formatted)

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
        self.assertEqual(first=response1.status_code, second=expect)
