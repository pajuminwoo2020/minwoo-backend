import logging

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q

logger = logging.getLogger('logger')


class Category(models.Model):
    TYPE_BOARD_NOTICE = 'notice'
    TYPE_BOARD_NOTICE_DISPLAY = '공지사항'
    TYPE_BOARD_ACTION = 'action'
    TYPE_BOARD_ACTION_DISPLAY = '민우뉴스'
    TYPE_BOARD_SOCIETY_ACTIVITY = 'society_activity'
    TYPE_BOARD_SOCIETY_ACTIVITY_DISPLAY = '소모임활동'
    TYPE_BOARD = (
        (TYPE_BOARD_NOTICE, TYPE_BOARD_NOTICE_DISPLAY),
        (TYPE_BOARD_ACTION, TYPE_BOARD_ACTION_DISPLAY),
        (TYPE_BOARD_SOCIETY_ACTIVITY, TYPE_BOARD_SOCIETY_ACTIVITY_DISPLAY),
    )

    name = models.CharField(max_length=255, blank=False)
    board_type = models.CharField(max_length=20, choices=TYPE_BOARD, null=False, blank=False)

    class Meta:
        verbose_name_plural = '게시판 카테고리 관리'

    def __str__(self):
        return f'[pk={self.pk}, name={self.name}, board_type={self.get_board_type_display()}]'
