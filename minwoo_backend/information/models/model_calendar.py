import logging

from django.db import models

logger = logging.getLogger('logger')


class Calendar(models.Model):
    schedule_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='일정 제목')
    schedule_from = models.DateTimeField(verbose_name='시작 시각')
    schedule_to = models.DateTimeField(verbose_name='종료 시각')
    memo = models.TextField(blank=True, null=True, verbose_name='일정 설명')

    class Meta:
        verbose_name_plural = '일정표 관리'
        verbose_name = '일정표 관리'

    def __str__(self):
        return f'[pk={self.pk}, schedule_name={self.schedule_name}, schedule_from={self.schedule_from}]'
