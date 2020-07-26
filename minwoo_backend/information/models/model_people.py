import logging

from django.db import models, transaction

from django.db.models import Q

logger = logging.getLogger('logger')

class People(models.Model) :
    name = models.CharField(max_length = 255, blank=False)
    position = models.CharField(max_length = 255, blank=False, help_text='직책')
    ordering= models.IntegerField(help_text='화면에 보여질 순서(낮은 숫자일수록 위에 보여짐)', null=True, blank=True)
    job = models.CharField(max_length = 255, blank=False, help_text='현재직업')

    class Meta:
        verbose_name_plural = '조직도 관리'
        ordering = ['ordering']

    def __str__(self):
        return f'[pk={self.pk}, name={self.name}, position={self.position}, job={self.job}]'
