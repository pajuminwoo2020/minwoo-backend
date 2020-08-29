import logging

from django.db import models, transaction
from django.db.models import Q

from board.models import Image

logger = logging.getLogger('logger')

class People(models.Model) :
    name = models.CharField(max_length = 255, blank=False, verbose_name='이름')
    position = models.CharField(max_length = 255, blank=False, help_text='직책', verbose_name='직책')
    ordering= models.IntegerField(help_text='화면에 보여질 순서(낮은 숫자일수록 위에 보여짐)', null=True, blank=True, verbose_name='순서')
    job = models.CharField(max_length = 255, blank=True, null=True, help_text='현재직업', verbose_name='직업')

    class Meta:
        verbose_name_plural = '조직도 관리'
        verbose_name = '조직도 관리'
        ordering = ['ordering']

    def __str__(self):
        return f'[pk={self.pk}, name={self.name}, position={self.position}, job={self.job}]'

class PeopleImage(Image):

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = '조직도 사진 업로드'
        verbose_name = '조직도 사진 업로드'
