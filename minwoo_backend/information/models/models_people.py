import logging

from django.db import models, transaction

from django.db.models import Q

logger = logging.getLogger('logger')

class People(models.Model) :
    name = models.CharField(max_length = 255, blank=False)
    position = models.CharField(max_length = 255, blank=False)
    department = models.CharField(max_length = 255, blank=False)
    
    def __str__(self):
        return loaction_name

