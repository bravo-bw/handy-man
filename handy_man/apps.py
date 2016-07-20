# myapp/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .signals import create_notice_types


class HandyManAppConfig(AppConfig):
    name = 'HandyMan'
    verbose_name = 'Handy Man'

    def ready(self):
        post_migrate.connect(create_notice_types, sender=self)
