from django.contrib import admin

from django.contrib.admin import ModelAdmin

from ..models import UserProfile
from ..actions import verify_user_profile


class UserProfileAdmin(ModelAdmin):

    actions = [verify_user_profile, ]

    list_filter = ['administrator_validated', 'email_validated', 'gender']

#     list_display = ['user__username', 'get_user.first_name', 'user__last_name', 'mobile', 'alter_contact', 'omang',
#                     'administrator_validated', 'email_validated']
    list_display = ['user_name', 'first_name', 'last_name', 'ratings', 'mobile', 'alter_contact', 'omang', 'administrator_validated', 'email_validated']

#     fields = []


#     radio_fields = {
#         "language": admin.VERTICAL,
#     }

    search_fields = ['mobile', 'alter_contact', 'omang', 'user__username', 'user__first_name', 'user_last_name']

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'username'

    def first_name(self, obj):
        return obj.user.first_name
    user_name.short_description = 'first_name'

    def last_name(self, obj):
        return obj.user.last_name
    user_name.short_description = 'last_name'


admin.site.register(UserProfile, UserProfileAdmin)
