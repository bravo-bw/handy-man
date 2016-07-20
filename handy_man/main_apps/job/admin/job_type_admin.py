from django.contrib import admin

from django.contrib.admin import ModelAdmin

from ..models import JobType


class JobTypeAdmin(ModelAdmin):
    pass
admin.site.register(JobType, JobTypeAdmin)
