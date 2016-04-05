from django.contrib import admin
from django.contrib.admin import ModelAdmin

from ..models import UserProfile


from ..models import Job


class JobAdmin(ModelAdmin):
    pass

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            if db_field.name == "sumbittor":
                kwargs["queryset"] = UserProfile.objects.filter(id__exact=request.GET.get('sumbittor', 0))
            return super(JobAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        except:
            pass

admin.site.register(Job, JobAdmin)
