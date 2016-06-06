from django import forms

from handy_man.apps.user_profile.models import UserProfile

from ..models import Job, JobType


class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        job_type_id = kwargs.pop('job_type')
        posted_by_id = kwargs.pop('posted_by_id')
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['job_type'].queryset = forms.ModelChoiceField(queryset=JobType.objects.filter(id=job_type_id))
        self.fields['posted_by'].queryset = forms.ModelChoiceField(queryset=UserProfile.objects.filter(id=posted_by_id))

    class Meta:
        model = Job
        fields = '__all__'
