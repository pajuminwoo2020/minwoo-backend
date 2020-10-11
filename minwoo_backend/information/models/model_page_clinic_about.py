import logging

from django.db import models
from board.models import ResizedImageField

class ClinicAbout(models.Model) :
    counseling = models.TextField(blank=True, null=True, verbose_name='상담 및 지원')
    counseling_title = models.CharField(max_length=20, blank=True, null=True, verbose_name='상담 및 지원 제목')
    counseling_image = ResizedImageField(blank=True, null=True, max_length=2048, verbose_name='상담 및 지원 이미지')
    education = models.TextField(blank=True, null=True, verbose_name='교육 활동')
    education_title = models.CharField(max_length=20, blank=True, null=True, verbose_name='교육활동 제목')
    education_image = ResizedImageField(blank=True, null=True, max_length=2048, verbose_name='교육활동 이미지')
    activity = models.TextField(blank=True, null=True, verbose_name='반성폭력활동')
    activity_title = models.CharField(max_length=20, blank=True, null=True, verbose_name='반성폭력활동 제목')
    activity_image = ResizedImageField(blank=True, null=True, max_length=2048, verbose_name='반성폭력활동 이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '[페이지수정]상담소 소개'
        verbose_name_plural = '[페이지수정]상담소 소개 추가'
        ordering = ['-created_at']

    def __str__(self):
        return f'[pk={self.pk}, activity={self.activity}]'
