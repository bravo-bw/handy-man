from django.conf.urls import patterns, url, include
# from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from handy_man.apps.user_profile.views import (user_profile, users, login_view, signup, logout_view,
                                               verify_account, Home)


urlpatterns = [
    url(r'^users/$', users),
    url(r'^verify/(?P<username>\w{0,30})$', verify_account),
    url(r'^users/(?P<username>\w{0,30})/$', users),
    url(r'^user_profile/(?P<username>\w{0,30})/$', user_profile, name='user_profile'),
    url(r'^user_profile/$', user_profile),
]
