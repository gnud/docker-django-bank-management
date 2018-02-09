from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from schwifty import IBAN
from social_django.models import AbstractUserSocialAuth


def validate_iban(value):
    try:
        IBAN(value)
    except ValueError:
        raise ValidationError(
            _('%(value)s is not a valid IBAN'),
            params={'value': value},
        )


class Userdata(models.Model):
    # Fields
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # http://www.xe.com/ibancalculator/faq.php
    iban = models.CharField(max_length=34, validators=[validate_iban])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)


def changed_patch(*args, **kwargs):
    user = args[0]

    user.is_staff = True

    social_admin_permissions = [
        'add_userdata',
        'change_userdata',
        'delete_userdata',
    ]

    for perm_name in social_admin_permissions:
        permission = Permission.objects.get(codename=perm_name)
        user.user_permissions.add(permission)
    user.save()


AbstractUserSocialAuth.changed = changed_patch
