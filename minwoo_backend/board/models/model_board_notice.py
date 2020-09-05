import logging

from django.db import models

from board.models import BoardBase

logger = logging.getLogger('logger')


class BoardNotice(BoardBase):
    created_by = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL, related_name='board_notices')
    thumbnail_source = models.CharField(blank=True, null=True, max_length=255)
    category = models.ForeignKey('board.Category', null=True, on_delete=models.SET_NULL, related_name='board_notices')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[pk={self.pk}, title={self.title}]'
