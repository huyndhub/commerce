from django.contrib import admin

from apps.app_base.utils import decrypt, encrypt

from .models import Personal, BlacklistToken
from .forms import PersonalForm


class PersonalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_decode', 'email', 'gender', 'date_of_birth', 'created_at', 'updated_at', ]
    list_display_links = ['id', 'name_decode', ]
    form = PersonalForm

    def save_model(self, request, obj, form, change):
        obj.full_name = encrypt(obj.full_name)
        obj.save()

        super(PersonalAdmin, self).save_model(request, obj, form, change)

    def name_decode(self, obj):
        return decrypt(obj.full_name) if obj.full_name else '-'

    def get_form(self, request, obj=None, **kwargs):
        base_form = super(PersonalAdmin, self).get_form(request, obj, **kwargs)

        class PersonalFormWithRequest(base_form):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['obj'] = obj
                return base_form(*args, **kwargs)

        return PersonalFormWithRequest

    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

    name_decode.short_description = "Họ tên"


admin.site.register(Personal, PersonalAdmin)
admin.site.register(BlacklistToken)
