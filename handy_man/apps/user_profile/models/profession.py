from django.db import models

from ...main.choices import ARTISAN_PROFESSION


class Profession(models.Model):

    profession_type = models.CharField(
        max_length=20,
        choices=ARTISAN_PROFESSION,
        null=True,
        blank=True)

    qualified = models.BooleanField(
        default=False,
        help_text="updated by admin save method only")

    def __str__(self):
        return self.profession_type

    class Meta:
        app_label = 'user_profile'
        unique_together = (('profession_type'),)
