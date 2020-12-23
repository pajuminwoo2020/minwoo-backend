import logging

from django.db import models
from django.utils import timezone

from board.models import Image

logger = logging.getLogger('logger')


class DonationButtonImage(Image):
    class Meta:
        verbose_name_plural = '버튼 이미지(후원하기)'
        verbose_name = '버튼 이미지(후원하기)'


class AffiliateButtonImage(Image):
    class Meta:
        verbose_name_plural = '버튼 이미지(상담소)'
        verbose_name = '버튼 이미지(상담소)'
