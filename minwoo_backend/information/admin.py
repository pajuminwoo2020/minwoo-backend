from django.contrib import admin
from django.utils.safestring import mark_safe

from information.models import Banner, BannerSmall, BannerLarge, Donation, Calendar, HistoryMain, SocietyAbout, People, Information, About, ClinicAbout, DonationPage, PeopleImage


class DonationAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'applicant_phone', 'price', 'donation_type', 'is_checked', 'created_at', 'download']
    list_filter = ['is_checked']
    search_fields = ['applicant_name', 'account_holder_name', 'email', 'applicant_phone', 'account_holder_phone']
    ordering = ('-created_at', )

    def download(self, obj):
        return mark_safe(f"<a href='{obj.get_absolute_url()}' class='import_link'>신청서 다운로드</a>")


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['id', 'schedule_name', 'schedule_from', 'schedule_to']
    search_fields = ['schedule_name']


class HistoryAdmin(admin.ModelAdmin):
    ordering = ('-date_at', )


class PeopleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'ordering']
    search_fields = ['name']


class BannerSmallAdmin(admin.ModelAdmin):
    readonly_fields = ('banner_type',)

    def get_queryset(self, request):
        qs = super(BannerSmallAdmin, self).get_queryset(request)

        return qs.filter(banner_type=Banner.TYPE_SMALL)

    def get_changeform_initial_data(self, request):
        return {'banner_type': Banner.TYPE_SMALL}


class BannerLargeAdmin(admin.ModelAdmin):
    readonly_fields = ('banner_type',)

    def get_queryset(self, request):
        qs = super(BannerLargeAdmin, self).get_queryset(request)

        return qs.filter(banner_type=Banner.TYPE_LARGE)

    def get_changeform_initial_data(self, request):
        return {'banner_type': Banner.TYPE_LARGE}


class InformationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_information.html'
    list_display = ['id', 'chief_executive', 'email', 'phone', 'fax', 'created_at']


class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'introduction', 'watchword', 'created_at']


class ClinicAboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'purpose', 'activity', 'created_at']


class DonationPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'introduction', 'benefits', 'created_at']

admin.site.register(BannerSmall, BannerSmallAdmin)
admin.site.register(BannerLarge, BannerLargeAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(HistoryMain, HistoryAdmin)
admin.site.register(SocietyAbout)
admin.site.register(People, PeopleAdmin)
admin.site.register(PeopleImage)
admin.site.register(Information, InformationAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(ClinicAbout, ClinicAboutAdmin)
admin.site.register(DonationPage, DonationPageAdmin)
