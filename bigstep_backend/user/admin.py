from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ['id', 'userid', 'fullname', 'language', 'timezone', 'is_active', 'created_at']
    list_filter = ['is_active']
    list_max_show_all = 5000
    search_fields = ['userid', 'fullname']
    ordering = ['created_at']


admin.site.register(User, UserAdmin)
