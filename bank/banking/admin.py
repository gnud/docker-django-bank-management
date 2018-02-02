from django.contrib import admin
from django import forms
from .models import Userdata

# Register your models here.


# noinspection SpellCheckingInspection
class UserdataAdminForm(forms.ModelForm):
    class Meta:
        model = Userdata
        fields = '__all__'


# noinspection SpellCheckingInspection
class UserdataAdmin(admin.ModelAdmin):
    form = UserdataAdminForm
    list_display = ['first_name', 'last_name', 'iban', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

    def get_queryset(self, request):
        return Userdata.objects.filter(owner=request.user)


admin.site.register(Userdata, UserdataAdmin)
