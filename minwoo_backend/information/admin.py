from django.contrib import admin

from information.models import Banner, Donation


class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'phone', 'email', 'price', 'donation_type', 'period', 'bank_account', 'address', 'is_checked']

admin.site.register(Banner)
admin.site.register(Donation, DonationAdmin)
