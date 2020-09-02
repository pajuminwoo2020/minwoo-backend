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

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='배너 제목')
    href = models.CharField(max_length=255, blank=False, help_text='배너 클릭시 이동할 주소(예시: https://www.naver.com)', verbose_name='배너주소')
    banner_type = models.CharField(max_length=10, choices=TYPE, default=TYPE_LARGE, blank=False, verbose_name='배너타입')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[pk={self.pk}, href={self.href}, banner_type={self.banner_type}]'


class BannerSmall(Banner):
    class Meta:
        verbose_name_plural = '배너업로드(작은사이즈)'
        verbose_name = '배너업로드(작은사이즈)'
        proxy = True


class BannerLarge(Banner):
    class Meta:
        verbose_name_plural = '배너업로드(큰사이즈)'
        verbose_name = '배너업로드(큰사이즈)'
        proxy = True
