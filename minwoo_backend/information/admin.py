from django.contrib import admin
from django.utils.safestring import mark_safe

from information.models import Banner, BannerSmall, BannerLarge, Donation, Calendar, HistoryMain, HistoryAffiliate, SocietyAbout, Information, About, ClinicAbout, DonationPage, PeopleImage, DonationButtonImage, AffiliateButtonImage


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
    list_display = ['title', 'image_file', 'href']

    def get_queryset(self, request):
        qs = super(BannerSmallAdmin, self).get_queryset(request)

        return qs.filter(banner_type=Banner.TYPE_SMALL)

    def get_changeform_initial_data(self, request):
        return {'banner_type': Banner.TYPE_SMALL}

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {'image_file': '이미지 크기(200 x 40)'}
        kwargs.update({'help_texts': help_texts})

        return super(BannerSmallAdmin, self).get_form(request, obj, **kwargs)


class BannerLargeAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_file', 'href', 'date_from', 'date_to']

    def get_queryset(self, request):
        qs = super(BannerLargeAdmin, self).get_queryset(request)

        return qs.filter(banner_type=Banner.TYPE_LARGE)

    def get_changeform_initial_data(self, request):
        return {'banner_type': Banner.TYPE_LARGE}

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {'image_file': '이미지 크기(723 x 395)'}
        kwargs.update({'help_texts': help_texts})

        return super(BannerLargeAdmin, self).get_form(request, obj, **kwargs)


class InformationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_information.html'
    list_display = ['chief_executive', 'email', 'phone', 'fax', 'created_at']


class AboutAdmin(admin.ModelAdmin):
    list_display = ['introduction', 'watchword', 'created_at']


class PeopleImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_file', 'created_at']

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {'image_file': '이미지 크기(제한 없음)'}
        kwargs.update({'help_texts': help_texts})

        return super(PeopleImageAdmin, self).get_form(request, obj, **kwargs)


class ClinicAboutAdmin(admin.ModelAdmin):
    list_display = ['counseling', 'education', 'activity', 'created_at']


class SocietyAboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {'image_file': '이미지 크기(제한 없음)'}
        kwargs.update({'help_texts': help_texts})

        return super(SocietyAboutAdmin, self).get_form(request, obj, **kwargs)


class DonationPageAdmin(admin.ModelAdmin):
    list_display = ['introduction', 'benefits', 'created_at']


class DonationButtonImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_file', 'created_at']

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {'image_file': '이미지 크기(230 x 135)'}
        kwargs.update({'help_texts': help_texts})

        return super(DonationButtonImageAdmin, self).get_form(request, obj, **kwargs)


class AffiliateButtonImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_file', 'created_at']

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {'image_file': '이미지 크기(230 x 135)'}
        kwargs.update({'help_texts': help_texts})

        return super(AffiliateButtonImageAdmin, self).get_form(request, obj, **kwargs)


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
admin.site.register(DonationButtonImage, DonationButtonImageAdmin)
admin.site.register(AffiliateButtonImage, AffiliateButtonImageAdmin)
