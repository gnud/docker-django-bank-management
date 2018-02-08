from django.contrib import admin
from django import forms
from .models import Userdata


class UserdataAdminForm(forms.ModelForm):
    class Meta:
        model = Userdata
        fields = '__all__'


class UserdataAdmin(admin.ModelAdmin):
    form = UserdataAdminForm
    list_display = ['first_name', 'last_name', 'iban', 'created', 'last_updated']
    fields = ['first_name', 'last_name', 'iban']
    readonly_fields = ['owner', 'created', 'last_updated']

    def get_queryset(self, request):
        return Userdata.objects.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user

        obj.save()


admin.site.register(Userdata, UserdataAdmin)
