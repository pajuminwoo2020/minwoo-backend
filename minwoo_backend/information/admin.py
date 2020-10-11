from django.contrib import admin
from django.utils.safestring import mark_safe

from information.models import Banner, BannerSmall, BannerLarge, Donation, Calendar, HistoryMain, HistoryAffiliate, SocietyAbout, Information, About, ClinicAbout, DonationPage, PeopleImage


class DonationAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'applicant_phone', 'price', 'donation_type', 'is_checked', 'created_at', 'download']
    list_filter = ['is_checked']
    search_fields = ['applicant_name', 'account_holder_name', 'email', 'applicant_phone', 'account_holder_phone']
    ordering = ('-created_at', )

    def download(self, obj):
        return mark_safe(f"<a href='{obj.get_absolute_url()}' class='import_link'>신청서 다운로드</a>")


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['schedule_name', 'schedule_from', 'schedule_to']
    search_fields = ['schedule_name']


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['memo', 'date_at']
    ordering = ('-date_at', )


class BannerSmallAdmin(admin.ModelAdmin):
    readonly_fields = ('banner_type',)
    list_display = ['title', 'image_file', 'href']

    def get_queryset(self, request):
        qs = super(BannerSmallAdmin, self).get_queryset(request)

        return qs.filter(banner_type=Banner.TYPE_SMALL)

    def get_changeform_initial_data(self, request):
        return {'banner_type': Banner.TYPE_SMALL}


class BannerLargeAdmin(admin.ModelAdmin):
    readonly_fields = ('banner_type',)
    list_display = ['title', 'image_file', 'href']

    def get_queryset(self, request):
        qs = super(BannerLargeAdmin, self).get_queryset(request)

        return qs.filter(banner_type=Banner.TYPE_LARGE)

    def get_changeform_initial_data(self, request):
        return {'banner_type': Banner.TYPE_LARGE}


class InformationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_information.html'
    list_display = ['chief_executive', 'email', 'phone', 'fax', 'created_at']


class AboutAdmin(admin.ModelAdmin):
    list_display = ['introduction', 'watchword', 'created_at']


class PeopleImageAdmin(admin.ModelAdmin):
    list_display = ['image_file', 'created_at']


class ClinicAboutAdmin(admin.ModelAdmin):
    list_display = ['counseling', 'education', 'activity', 'created_at']


class SocietyAboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class DonationPageAdmin(admin.ModelAdmin):
    list_display = ['introduction', 'benefits', 'created_at']

admin.site.register(BannerSmall, BannerSmallAdmin)
admin.site.register(BannerLarge, BannerLargeAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(HistoryMain, HistoryAdmin)
admin.site.register(HistoryAffiliate, HistoryAdmin)
admin.site.register(SocietyAbout, SocietyAboutAdmin)
admin.site.register(PeopleImage, PeopleImageAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(ClinicAbout, ClinicAboutAdmin)
admin.site.register(DonationPage, DonationPageAdmin)
