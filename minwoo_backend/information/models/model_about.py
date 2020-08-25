import logging

from django.db import models

class About(models.Model) :
    introduction = models.TextField(blank=False, verbose_name='소개')
    watchword = models.TextField(blank=False, verbose_name='회원 다짐')
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now or auto_now_add?

    class Meta:
        verbose_name = '민우회 소개'
        verbose_name_plural = '민우회 소개 추가'
        ordering = ['-created_at']

    def __str__(self):
        return f'[pk={self.pk}, introduction={self.introduction}, watchword={self.watchword}]'