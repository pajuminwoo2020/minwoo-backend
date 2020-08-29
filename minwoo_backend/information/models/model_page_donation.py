import logging

from django.db import models

class DonationPage(models.Model) :
    introduction = models.TextField(blank=False, verbose_name='기부소개')
    benefits = models.TextField(blank=False, verbose_name='회원이 되면')
    payment_method = models.TextField(blank=False, verbose_name='회비 납부 방법')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '[페이지수정]기부 소개'
        verbose_name_plural = '[페이지수정]기부 소개 추가'
        ordering = ['-created_at']

    def __str__(self):
        return f'[pk={self.pk}, introduction={self.introduction}]'
