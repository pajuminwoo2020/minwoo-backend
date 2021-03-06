import logging

from django.db import models

from board.models import BoardBase

logger = logging.getLogger('logger')


class BoardDrive(BoardBase):
    created_by = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL, related_name='board_drives')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[pk={self.pk}, title={self.title}]'
