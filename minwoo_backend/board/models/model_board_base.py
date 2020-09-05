import logging
from PIL import Image as PILImage
from io import BytesIO

from hitcount.models import HitCountMixin, HitCount
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q

from app.common.utils import image_directory_path

logger = logging.getLogger('logger')


class BoardBase(models.Model, HitCountMixin):
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(blank=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    files = GenericRelation('board.File', content_type_field='board_at_type', object_id_field='board_at_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ResizedImageFieldFile(models.ImageField.attr_class):
    def save(self, name, content, save=True):
        # 이미지 파일이 500kb 이상이면 압축
        if content.file and content.file.read() and content.file.tell() > 500000:
            content.file.seek(0)
            image_temporary = PILImage.open(content.file)
            image_temporary = image_temporary.convert('RGB')
            new_content = BytesIO()
            image_temporary.save(new_content, format='JPEG', quality=50)
            name = image_directory_path(name, 'jpg')
        else:
            name = image_directory_path(name)
            new_content = content.file

        new_content.seek(0)
        super(ResizedImageFieldFile, self).save(name, new_content, save)


class ResizedImageField(models.ImageField):
    """
    이미지 크기가 크면 줄여서 저장하기 위한 custom ImageField
    """
    attr_class = ResizedImageFieldFile
