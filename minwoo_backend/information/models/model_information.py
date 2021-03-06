import logging

from django.db import models

logger = logging.getLogger('logger')


class Information(models.Model):
    membership_management = models.CharField(max_length=255, blank=False, verbose_name='회원팀 활동가')
    membership_management_email = models.CharField(max_length=255, blank=False, verbose_name='회원팀 이메일')
    membership_management_phone = models.CharField(max_length=255, blank=False, verbose_name='회원팀 전화번호')
    chief_executive = models.CharField(max_length=255, blank=False, verbose_name='대표자')
    address_street = models.CharField(max_length=255, blank=True, null=True, verbose_name='도로명 주소')
    address_jibun = models.CharField(max_length=255, blank=True, null=True, verbose_name='지번 주소')
    location_subway = models.TextField(blank=True, null=True, verbose_name='지하철 이용')
    location_bus = models.TextField(blank=True, null=True,verbose_name='버스 이용')
    location_car = models.TextField(blank=True, null=True,verbose_name='차량 이용')
    registration_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='사업자등록 번호')
    email = models.CharField(max_length=255, blank=False, verbose_name='민우회 이메일')
    phone = models.CharField(max_length=255, blank=False, verbose_name='민우회 전화번호')
    fax = models.CharField(max_length=255, blank=False, verbose_name='민우회 팩스')
    bank_account = models.CharField(max_length=255, blank=False, verbose_name='후원계좌')
    instagram_feed = models.CharField(max_length=255, blank=True, null=True, verbose_name='인스타그램 게시물 주소', help_text="메인화면 인스타그램 미리보기 게시물")
    location_latitude = models.DecimalField(max_digits = 7, null=True, decimal_places=4, verbose_name='위도')
    location_longitude = models.DecimalField(max_digits = 7, null=True, decimal_places=4, verbose_name='경도')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name_plural = '기본 정보 관리'
        verbose_name = '기본 정보 관리'
        ordering = ('-created_at',)

    def __str__(self):
        return f'[pk={self.pk}, name={self.chief_executive}, email={self.email}, phone={self.phone}, fax={self.fax}]'
