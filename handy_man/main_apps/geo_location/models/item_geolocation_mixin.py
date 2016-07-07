from django.db import models
from django_extensions.db.models import TimeStampedModel

from .location_divisions import Street, TownVillage, District
# from ..choices import *
# from ..classes import Geolocation


class ItemGeolocationMixin(TimeStampedModel):

    latitude = models.FloatField(
        verbose_name='Latitude',
        max_length=50,
        null=True,
        blank=True,)

    longitude = models.FloatField(
        verbose_name='Longitude',
        max_length=50,
        null=True,
        blank=True,)

    street = models.ForeignKey(Street, on_delete=models.CASCADE, blank=True, null=True,)

    town_village = models.ForeignKey(TownVillage, on_delete=models.CASCADE, blank=True, null=True,)

    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True,)

    def save(self, *args, **kwargs):
#         geolocation = Geolocation()

#         geolocation.point_inside_polygon(self.latitude, self.longitude, poly)
        super(ItemGeolocationMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
