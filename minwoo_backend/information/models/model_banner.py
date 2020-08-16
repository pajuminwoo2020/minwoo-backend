import logging

from django.db import models

from board.models import Image

logger = logging.getLogger('logger')


class Banner(Image):
    TYPE_SMALL = 'small'
    TYPE_SMALL_DISPLAY = '하단 작은 배너'
    TYPE_LARGE = 'large'
    TYPE_LARGE_DISPLAY = '상단 큰 배너'
    TYPE = (
        (TYPE_SMALL, TYPE_SMALL_DISPLAY),
        (TYPE_LARGE, TYPE_LARGE_DISPLAY),
    )

    href = models.CharField(max_length=255, blank=False)
    banner_type = models.CharField(max_length=10, choices=TYPE, default=TYPE_LARGE, blank=False)

    class Meta:
        verbose_name_plural = '배너업로드(큰사이즈: 720*320, 작은사이즈: 300*100)'
        ordering = ['-created_at']

    def __str__(self):
        return f'[pk={self.pk}, href={self.href}, banner_type={self.banner_type}]'
