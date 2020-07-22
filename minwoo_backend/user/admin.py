from django.contrib import admin
from django.contrib.auth.models import Group

from user.models import User


class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ['id', 'userid', 'fullname', 'is_active', 'group', 'last_login', 'created_at']
    list_filter = ['is_active']
    list_max_show_all = 5000
    search_fields = ['userid', 'fullname']
    ordering = ['created_at']
    exclude = ['user_permissions', 'fullname_en', 'language', 'timezone', 'is_superuser', 'password', 'last_login']

    def group(self, obj):
        return obj.get_groups();


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
