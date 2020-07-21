import logging

from django.db import models

logger = logging.getLogger('logger')

class SocietyAbout(models.Model):
    name = models.CharField(max_length=255, blank=False)
    activity = models.TextField(blank=True)

    def __str__(self):
        return f'[pk={self.pk}, name={self.name}]'