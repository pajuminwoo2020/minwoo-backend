import logging

from django.db import models
from django.db.models.signals import pre_delete
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.urls import reverse

logger = logging.getLogger('logger')


class File(models.Model):
    file = models.FileField(blank=False, null=False, max_length=2048)
    file_name = models.CharField(max_length=255, blank=True)
    board_at_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    board_at_id = models.PositiveIntegerField(null=True)
    board_at = GenericForeignKey('board_at_type', 'board_at_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[pk={self.pk}, title={self.file_name}]'

    def get_absolute_url(self):
        return reverse('board:file', kwargs={'file_id': self.pk})


@receiver(pre_delete, sender=File)
def delete_file_hook(sender, instance, using, **kwargs):
    instance.file.delete()
