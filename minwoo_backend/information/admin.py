from django.contrib import admin

from information.models import Banner, Donation, Calendar, InformationHistory


class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'phone', 'email', 'price', 'donation_type', 'period', 'bank_account', 'address', 'is_checked']
    list_filter = ['is_checked']
    search_fields = ['user_name', 'email', 'phone']


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['id', 'schedule_name', 'schedule_from', 'schedule_to']
    search_fields = ['schedule_name']


admin.site.register(Banner)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(InformationHistory)
