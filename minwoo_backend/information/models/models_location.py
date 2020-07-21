import logging

from django.db import models, transaction

from django.db.models import Q

logger = logging.getLogger('logger')

class InformationLocation(models.Model) :
    location_name = models.CharField(max_length = 255, blank=False)
    location_roadname = models.CharField(max_length = 255, blank=False)
    location_lotnumber = models.CharField(max_length = 255, blank=False)
    byTrain = models.TextField(blank=False)
    byBus = models.TextField(blank=False)
    byCar = models.TextField(blank=False)

    def __str__(self):
        return loaction_name
