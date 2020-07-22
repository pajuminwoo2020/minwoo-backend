import logging

from django.db import models

logger = logging.getLogger('logger')

class SocietyAbout(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=True)
    schedule = models.TextField(blank=True, help_text="'-'로 줄을 구분하세요")
    main_activity = models.TextField(blank=True, help_text="'-'로 줄을 구분하세요")
    website = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '소모임 소개 추가'

    def __str__(self):
        return f'[pk={self.pk}, name={self.name}, is_default={self.is_default}]'
