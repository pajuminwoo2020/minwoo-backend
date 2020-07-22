import logging

from django.db import models

logger = logging.getLogger('logger')


class HistoryBase(models.Model):
    memo = models.CharField(max_length=255, blank=False)
    date_at = models.DateField()

    class Meta:
        abstract = True
        ordering = ['-date_at']

    def __str__(self):
        return f'[pk={self.pk}, memo={self.memo}, date_at={self.date_at}]'


class HistoryMain(HistoryBase):
    class Meta:
        verbose_name_plural = '민우회 연혁'


class HistoryAffiliate(HistoryBase):
    class Meta:
        verbose_name_plural = '성폭력상담소 연혁'
