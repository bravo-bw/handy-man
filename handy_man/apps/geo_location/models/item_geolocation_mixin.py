from django.db import models


class ItemGeolocationMixin(models.Model):

    latitude = models.FloatField()

    longitude = models.FloatField()

    class Meta:
        abstract = True
