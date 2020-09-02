import logging
import sys
from PIL import Image as PILImage
from io import BytesIO
import mimetypes

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

logger = logging.getLogger('logger')


class Image(models.Model):
    image_file = models.ImageField(blank=True, null=True, max_length=2048, verbose_name='이미지 파일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        ordering = ['created_at']

    def get_image_absolute_url(self):
        if self.image_file:
            return reverse('board:image', kwargs={'image_id': self.pk})

        return ''

    def save(self, *args, **kwargs):
        (mimetype, encoding) = mimetypes.guess_type(self.image_file.name if self.image_file else '')
        if mimetype and mimetype != 'image/jpeg':
            # png같은 이미지 파일은 용량이 너무 커서 줄여줌
            image_temporary = PILImage.open(self.image_file)
            image_temporary = image_temporary.convert('RGB')
            outputIoStream = BytesIO()
            image_temporary.save(outputIoStream , format='JPEG', quality=60)
            outputIoStream.seek(0)

            self.image_file = InMemoryUploadedFile(
                outputIoStream,
                'ImageField',
                "{}.jpg".format(self.image_file.name.split('.')[0]),
                'image/jpeg',
                sys.getsizeof(outputIoStream),
                None,
            )

        super(Image, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Image)
def delete_file_hook(sender, instance, using, **kwargs):
    if instance.image_file:
        instance.image_file.delete()
