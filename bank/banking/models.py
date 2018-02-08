from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save

from .signals import create_user_profile

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Userdata(models.Model):
    # Fields
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    iban = models.CharField(max_length=32, validators=[alphanumeric])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)


post_save.connect(create_user_profile, sender=get_user_model())
