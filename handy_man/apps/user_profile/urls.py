from django.conf.urls import patterns, url, include
# from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from handy_man.apps.user_profile.views import (user_profile, login_view, signup, logout_view, verify_account,
                                               user_profile_documents, RegisteredUsersView)


urlpatterns = [
#     url(r'^users/$', users),
    url(r'^verify/(?P<username>\w{0,30})$', verify_account),
#     url(r'^users/(?P<username>\w{0,30})/$', users),
    url(r'^user_profile/(?P<username>\w{0,30})/$', user_profile, name='user_profile'),
    url(r'^user_profile_doc/(?P<username>\w{0,30})/$', user_profile_documents, name='user_profile_documents'),
#     url(r'^user_profile/$', user_profile),
    url(r'^registered_users/$', RegisteredUsersView.as_view(), name='registered_users_url')
]
