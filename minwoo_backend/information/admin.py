from django.contrib import admin

from information.models import Banner
from information.models import InformationHistory

admin.site.register(Banner)
admin.site.register(InformationHistory)