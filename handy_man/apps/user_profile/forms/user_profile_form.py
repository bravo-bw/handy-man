from django.core.files.images import get_image_dimensions
from django import forms
from handy_man.apps.user_profile.models import UserProfile

from ...main.custom_form_fields import SubmitButtonField


class UserProfileForm(forms.ModelForm):
    avatar_image = forms.ImageField(required=False)
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Last Name'}))
    mobile = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'mobile number'}))
    alter_contact = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Alternative Contact'}))
    username = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Username'}))
    dob = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'readonly': 'readonly', 'placeholder': 'Date Of Birth'}))
#     submit_button = SubmitButtonField(label='Submit', initial="Submit")

#     def clean_avatar(self):
#         avatar = self.cleaned_data['avatar']
# 
#         try:
#             w, h = get_image_dimensions(avatar)
# 
#             max_width = max_height = 100
#             if w > max_width or h > max_height:
#                 raise forms.ValidationError(
#                     u'Please use an image that is '
#                     '%s x %s pixels or smaller.' % (max_width, max_height))
# 
#             main, sub = avatar.content_type.split('/')
#             if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
#                 raise forms.ValidationError(u'Please use a JPEG, '
#                                             'GIF or PNG image.')
# 
#             if len(avatar) > (20 * 1024):
#                 raise forms.ValidationError(
#                     u'Avatar file size may not exceed 20k.')
# 
#         except AttributeError:
#             """
#             Handles case when we are updating the user profile
#             and do not supply a new avatar
#             """
#             pass
# 
#         return avatar

    class Meta:
        fields = ['email', 'first_name', 'last_name']
        profile_fields = ['mobile', 'dob', 'alter_contact']
        model = UserProfile