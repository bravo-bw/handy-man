from django import forms

from handy_man.apps.user_profile.models import UserProfile

from ..models import Job, JobType


class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = '__all__'
