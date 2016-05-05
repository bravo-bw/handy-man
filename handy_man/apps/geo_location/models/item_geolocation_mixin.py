from django.db import models

from .location_divisions import Street, TownVillage, District
# from ..choices import *
# from ..classes import Geolocation


class ItemGeolocationMixin(models.Model):

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

    street = models.ForeignKey(Street, on_delete=models.CASCADE, null=True,)

    town_village = models.ForeignKey(TownVillage, on_delete=models.CASCADE, null=True,)

    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True,)

    def save(self, *args, **kwargs):
#         geolocation = Geolocation()

#         geolocation.point_inside_polygon(self.latitude, self.longitude, poly)
        super(ItemGeolocationMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
