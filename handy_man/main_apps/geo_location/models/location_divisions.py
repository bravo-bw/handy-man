from django.db import models


class District(models.Model):

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

    def __str__(self):
        return self.district_name

    class Meta:
        app_label = 'geo_location'
        unique_together = (('district_name', 'center_latitude', 'center_longitude'),)


class TownVillage(models.Model):

    district = models.ForeignKey(District, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.town_village_name

    class Meta:
        app_label = 'geo_location'
        unique_together = (('town_village_name', 'center_latitude', 'center_longitude'),)


class Street(models.Model):

    town_village = models.ForeignKey(TownVillage, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.street_name

    class Meta:
        app_label = 'geo_location'
        unique_together = (('street_name', 'center_latitude', 'center_longitude'),)
