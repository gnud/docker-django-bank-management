from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()

        socialadmin_permissions = [
            'add_userdata',
            'change_userdata',
            'delete_userdata',
        ]

        for perm_name in socialadmin_permissions :
            permission = Permission.objects.get(codename=perm_name)
            instance.user_permissions.add(permission)
