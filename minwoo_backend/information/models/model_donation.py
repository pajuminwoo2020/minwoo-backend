import logging

from django.db import models

logger = logging.getLogger('logger')


class Donation(models.Model):
    donation_type = models.CharField(max_length=255, blank=False, verbose_name='기부종류')
    price = models.IntegerField(verbose_name='기부금')
    period = models.IntegerField(verbose_name='기부 주기')
    user_name = models.CharField(max_length=255, blank=False, verbose_name='회원명')
    birthday = models.DateField(verbose_name='생년월일')
    phone = models.CharField(max_length=255, blank=False, verbose_name='휴대폰번호')
    email = models.CharField(max_length=255, blank=False, verbose_name='이메일')
    bank_account = models.CharField(max_length=255, blank=False, verbose_name='은행계좌')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='주소')
    memo = models.CharField(max_length=255, blank=True, null=True, verbose_name='기타 메모')
    is_checked = models.BooleanField(default=False, verbose_name='연락 여부', help_text='후원신청 확인후 회원에게 연락했으면 체크해주세요. 후원 신청에 대해 빠짐없이 연락하기 위한 용도입니다.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='신청일')

    class Meta:
        verbose_name_plural = '후원금 신청내역 관리'
        verbose_name = '후원금 신청내역 관리'
