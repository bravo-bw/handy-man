from django import forms

from ..models import Quote


class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ['currency', 'estimate_hours', 'rate_per_hour', 'amount']