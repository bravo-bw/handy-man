from django.db import models

from .location_divisions import Street, TownVillage, District


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

    street = models.ForeignKey(Street, on_delete=models.CASCADE)

    town_village = models.ForeignKey(TownVillage, on_delete=models.CASCADE)

    district = models.ForeignKey(District, on_delete=models.CASCADE)

    class Meta:
        abstract = True
