import logging

from django.db import models

logger = logging.getLogger('logger')


class Calendar(models.Model):
    schedule_name = models.CharField(max_length=255, blank=False, null=False)
    schedule_from = models.DateTimeField()
    schedule_to = models.DateTimeField()
    memo = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = '일정표 관리'

    def __str__(self):
        return f'[pk={self.pk}, schedule_name={self.schedule_name}, schedule_from={self.schedule_from}]'
