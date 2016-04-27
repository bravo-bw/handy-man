from django.db import models


class Street(models.Model):
    street_name = models.CharField(max_length=200)
    center_latitude = models.FloatField(
        verbose_name='Center Latitude',
        max_length=50,
        null=True,
        blank=True,)

    center_longitude = models.FloatField(
        verbose_name='Center Longitude',
        max_length=50,
        null=True,
        blank=True,)


class TownVillage(models.Model):
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    town_village_name = models.CharField(max_length=200)
    center_latitude = models.FloatField(
        verbose_name='Center Latitude',
        max_length=50,
        null=True,
        blank=True,)

    center_longitude = models.FloatField(
        verbose_name='Center Longitude',
        max_length=50,
        null=True,
        blank=True,)


class District(models.Model):
    town_village = models.ForeignKey(TownVillage, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=200)
    center_latitude = models.FloatField(
        verbose_name='Center Latitude',
        max_length=50,
        null=True,
        blank=True,)

    center_longitude = models.FloatField(
        verbose_name='Center Longitude',
        max_length=50,
        null=True,
        blank=True,)
