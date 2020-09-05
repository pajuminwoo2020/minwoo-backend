import logging
from PIL import Image as PILImage
from io import BytesIO

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.common.utils import image_directory_path
from board.models import ResizedImageField

logger = logging.getLogger('logger')


class Image(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    image_file = ResizedImageField(blank=True, null=True, max_length=2048, verbose_name='이미지 파일')

    class Meta:
        ordering = ['created_at']

    def get_image_absolute_url(self):
        if self.image_file:
            return self.image_file.url

        return ''


@receiver(pre_delete, sender=Image)
def delete_file_hook(sender, instance, using, **kwargs):
    if instance.image_file:
        instance.image_file.delete()
