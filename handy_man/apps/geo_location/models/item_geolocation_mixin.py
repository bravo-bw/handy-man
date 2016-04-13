from django.db import models


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

    street = models.CharField(
        verbose_name='Street name',
        max_length=50,
        null=True,
        blank=True,)

    town_village = models.CharField(
        verbose_name='Town or village name',
        max_length=50,
        null=True,
        blank=True,)

    district = models.CharField(
        verbose_name='District',
        max_length=50,
        null=True,
        blank=True,)

    class Meta:
        abstract = True
