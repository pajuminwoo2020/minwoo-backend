import logging

from django.db import models

from board.models import BoardBase
from board.models.model_category import Category

logger = logging.getLogger('logger')


class BoardAffiliateActivity(BoardBase):
    created_by = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL, related_name='board_affiliate_activities')
    thumbnail_source = models.CharField(blank=True, null=True, max_length=255)
    category = models.ForeignKey('board.Category', null=True, on_delete=models.SET_NULL, related_name='board_affiliate_activities')
    on_board_action = models.CharField(max_length=20, choices=Category.TYPE_BOARD, null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[pk={self.pk}, title={self.title}]'
