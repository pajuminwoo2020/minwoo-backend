from django.contrib import admin

from hitcount.models import HitCount, Hit, BlacklistIP, BlacklistUserAgent

admin.site.unregister(HitCount)
admin.site.unregister(Hit)
admin.site.unregister(BlacklistIP)
admin.site.unregister(BlacklistUserAgent)
