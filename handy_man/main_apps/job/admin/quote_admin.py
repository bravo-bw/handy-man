from django.contrib import admin

from django.contrib.admin import ModelAdmin

from ..models import Quote


class QuoteAdmin(ModelAdmin):
    pass
admin.site.register(Quote, QuoteAdmin)
