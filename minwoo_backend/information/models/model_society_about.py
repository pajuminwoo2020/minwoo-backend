import logging

from django.db import models

logger = logging.getLogger('logger')

class SocietyAbout(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='소모임명')
    description = models.CharField(max_length=255, blank=True, verbose_name='소모임 설명')
    schedule = models.TextField(blank=True, help_text="'-'로 줄을 구분하세요", verbose_name='소모임 정기 모임 날짜')
    main_activity = models.TextField(blank=True, help_text="'-'로 줄을 구분하세요", verbose_name='소모임 주요 활동')
    website = models.CharField(max_length=255, blank=True, verbose_name='소모임 홈페이지')

    class Meta:
        verbose_name_plural = '소모임 소개 추가'
        verbose_name = '소모임 소개 추가'

    def __str__(self):
        return f'[pk={self.pk}, name={self.name}]'
