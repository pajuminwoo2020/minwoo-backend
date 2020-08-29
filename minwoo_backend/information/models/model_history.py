import logging

from django.db import models

logger = logging.getLogger('logger')


class HistoryBase(models.Model):
    memo = models.CharField(max_length=255, blank=False, help_text='해당 날짜에 있었던 일', verbose_name='있었던 일')
    date_at = models.DateField(verbose_name='날짜')

    class Meta:
        abstract = True
        ordering = ['-date_at']

    def __str__(self):
        return f'[pk={self.pk}, memo={self.memo}, date_at={self.date_at}]'


class HistoryMain(HistoryBase):
    class Meta:
        verbose_name_plural = '민우회 연혁'
        verbose_name = '민우회 연혁'
