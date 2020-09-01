import logging

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse

logger = logging.getLogger('logger')


class Image(models.Model):
    image_file = models.ImageField(blank=True, null=True, max_length=2048, verbose_name='이미지 파일')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def get_image_absolute_url(self):
        if self.image_file:
            return reverse('board:image', kwargs={'image_id': self.pk})

        return ''


@receiver(pre_delete, sender=Image)
def delete_file_hook(sender, instance, using, **kwargs):
    if instance.image_file:
        instance.image_file.delete()
