import logging

from hitcount.models import HitCountMixin, HitCount
from django.db import models, transaction
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q

logger = logging.getLogger('logger')


class BoardBase(models.Model, HitCountMixin):
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(blank=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
