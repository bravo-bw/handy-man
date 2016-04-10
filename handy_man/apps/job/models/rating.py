from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):

    artisan = models.ForeignKey(User)

    current_rating = models.DecimalField(max_digits=10, decimal_places=2)

    previous_rating = models.DecimalField(max_digits=10, decimal_places=2)

    lowest_rating = models.DecimalField(max_digits=10, decimal_places=2)

    highest_rating = models.DecimalField(max_digits=10, decimal_places=2)
