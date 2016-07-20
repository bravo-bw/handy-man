from django import forms

from handy_man.main_apps.main.choices import CURRENCY
from handy_man.main_apps.user_profile.models import UserProfile

from handy_man.main_apps.job.models import Quote, Job


class QuotationForm(forms.ModelForm):

    currency = forms.ChoiceField(widget=forms.Select, choices=CURRENCY)
#     rate_per_hour = forms.DecimalField(widget=forms.widgets.NumberInput(attrs={'placeholder': 'Rate Per Hour'}))
    estimate_hours = forms.DecimalField(widget=forms.widgets.NumberInput(attrs={'placeholder': 'Estimate Hours'}))
    amount = forms.DecimalField(widget=forms.widgets.NumberInput(attrs={'placeholder': 'Amount'}))
    accepted = forms.CheckboxInput()
    job = forms.ModelChoiceField(queryset=Job.objects.all(), to_field_name='identifier')
    # Validating this causes a problem when unique_together is set in the model. Need to fix it so we have the
    # important unique_together.
    artisan = forms.ModelChoiceField(queryset=UserProfile.objects.all(), to_field_name='pk')

    class Meta:
        model = Quote
        fields = ['currency', 'estimate_hours', 'amount', 'job', 'accepted', 'artisan']