from django.contrib import admin

from .models import UserInfo, BlacklistToken


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'gender', 'date_of_birth', 'created_at', 'updated_at', ]
    list_display_links = ['id', 'full_name', ]
    readonly_fields = ('full_name', 'user', )

    def has_add_permission(self, request):
        return False


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(BlacklistToken)
