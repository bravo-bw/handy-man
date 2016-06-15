from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags

from ...main.choices import ACCOUNT_TYPE


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    mobile = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Mobile Number'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
    account_type = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Account Type'}))

    def is_valid(self):
        form = super(UserCreateForm, self)
        if not form.is_valid():
            for f, error in self.errors.items():
                if f != '__all_':
                    self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        profile_fields = ['mobile', 'account_type']
        model = User