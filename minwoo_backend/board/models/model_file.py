import logging
import random
import string

from django.db import models
from django.db.models.signals import pre_delete
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.dispatch import receiver
from django.urls import reverse

from app.common.utils import file_directory_path

logger = logging.getLogger('logger')


class File(models.Model):
    file = models.FileField(blank=False, null=False, max_length=2048, upload_to=file_directory_path)
    file_name = models.CharField(max_length=255, blank=True)
    board_at_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    board_at_id = models.PositiveIntegerField(null=True)
    board_at = GenericForeignKey('board_at_type', 'board_at_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[pk={self.pk}, title={self.file_name}, board_at={self.board_at_type}]'

    def get_absolute_url(self):
        """
        Id값만 인코딩하면 너무 짧아서 랜덤 스트링을 붙인 후에 인코딩한다
        """
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        uidb64_string = f'{random_str}{self.id}'

        return reverse('board:file', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(uidb64_string))})


@receiver(pre_delete, sender=File)
def delete_file_hook(sender, instance, using, **kwargs):
    instance.file.delete()
