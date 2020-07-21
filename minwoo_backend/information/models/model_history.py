import logging

from hitcount.models import HitCountMixin, HitCount
from django.db import models, transaction
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q

logger = logging.getLogger('logger')


class InformationHistory(models.Model, HitCountMixin):
    kind = models.IntegerField(default=0)
    year = models.IntegerField()
    body = models.TextField(blank=False)

    class Meta:
        ordering = ['year']
        verbose_name_plural = '연혁'

    def __str__(self):
        return f'[pk={self.pk}, kind={self.kind}, year={self.year}]'
