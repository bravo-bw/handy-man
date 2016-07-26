from django.contrib import admin

from django.contrib.admin import ModelAdmin

from ..models import Job
from ..forms import JobForm


class JobAdmin(ModelAdmin):
    form = JobForm

#     list_filter = ['posted_by', 'allocated_to', 'status', 'job_type']
# 
#     list_display = ['posted_by', 'allocated_to', 'identifier', 'status', 'job_type', 'description']
# 
#     search_fields = ['posted_by', 'allocated_to', 'identifier', 'status', 'job_type']

admin.site.register(Job, JobAdmin)
