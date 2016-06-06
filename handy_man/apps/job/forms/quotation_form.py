from django import forms

from handy_man.apps.main.choices import CURRENCY

from ..models import Quote, Job


class QuotationForm(forms.ModelForm):

    currency = forms.ChoiceField(widget=forms.Select, choices=CURRENCY)
    rate_per_hour = forms.DecimalField(widget=forms.widgets.NumberInput(attrs={'placeholder': 'Rate Per Hour'}))
    estimate_hours = forms.DecimalField(widget=forms.widgets.NumberInput(attrs={'placeholder': 'Estimate Hours'}))
    amount = forms.DecimalField(widget=forms.widgets.NumberInput(attrs={'placeholder': 'Amount'}))
    accepted = forms.CheckboxInput()
    job = forms.ModelChoiceField(queryset=Job.objects.all(), to_field_name='pk')

    class Meta:
        model = Quote
        fields = ['currency', 'estimate_hours', 'rate_per_hour', 'amount', 'job', 'accepted']