from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.validators import RegexValidator
from django.db import models

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


class CustomUser(get_user_model()):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.pk:
            super(CustomUser, self).is_staff = True

            social_admin_permissions = [
                'add_userdata',
                'change_userdata',
                'delete_userdata',
            ]

            for perm_name in social_admin_permissions:
                permission = Permission.objects.get(codename=perm_name)
                self.user_permissions.add(permission)

        super(CustomUser, self).save(args, kwargs)
