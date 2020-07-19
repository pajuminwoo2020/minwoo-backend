import logging

from django.db import models

logger = logging.getLogger('logger')


class Donation(models.Model):
    donation_type = models.CharField(max_length=255, blank=False)
    price = models.IntegerField()
    period = models.IntegerField()
    user_name = models.CharField(max_length=255, blank=False)
    birthday = models.DateField()
    phone = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, blank=False)
    bank_account = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    memo = models.CharField(max_length=255, blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '후원금 신청내역 관리'
