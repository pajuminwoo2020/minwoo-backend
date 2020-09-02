import logging

from django.db import models

class ClinicAbout(models.Model) :
    purpose = models.TextField(blank=False, verbose_name='설립 취지')
    activity = models.TextField(blank=False, verbose_name='활동 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '[페이지수정]상담소 소개'
        verbose_name_plural = '[페이지수정]상담소 소개 추가'
        ordering = ['-created_at']

    def __str__(self):
        return f'[pk={self.pk}, purpose={self.purpose}, activity={self.activity}]'
