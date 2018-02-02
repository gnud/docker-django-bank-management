from django.test import TestCase

# Create your tests here.
from .models import Userdata


class UserdataModelTest(TestCase):
    def test_string_representation(self):
        entry = Userdata(first_name="John", last_name="Doe")
        self.assertEqual(str(entry), "%s %s" % (entry.first_name, entry.last_name))
