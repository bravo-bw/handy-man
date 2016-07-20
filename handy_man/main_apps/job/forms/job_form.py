from django import forms

from handy_man.main_apps.job.models import Job


class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = '__all__'
