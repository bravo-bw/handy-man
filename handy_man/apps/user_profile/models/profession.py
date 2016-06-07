from django.db import models

from ...main.choices import ARTISAN_PROFESSION


class Profession(models.Model):

    code = models.CharField(
        max_length=5
    )

    profession_type = models.CharField(
        max_length=20,
        choices=ARTISAN_PROFESSION,
        unique=True)

    def __str__(self):
        return self.profession_type

    class Meta:
        app_label = 'user_profile'
