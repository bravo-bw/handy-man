from django.conf.urls import url
from django.contrib import admin
# from django.contrib.auth.decorators import login_required
from handy_man.main_apps.user_profile.views import (
    user_profile, verify_account, user_profile_documents,
    RegisteredUsersView, user_profile_geolocation)


urlpatterns = [
#     url(r'^users/$', users),
    url(r'^verify/(?P<username>\w{0,30})$', verify_account),
#     url(r'^users/(?P<username>\w{0,30})/$', users),
    url(r'^user_profile/(?P<username>\w{0,30})/$', user_profile, name='user_profile'),
    url(r'^user_profile_doc/(?P<username>\w{0,30})/$', user_profile_documents, name='user_profile_documents'),
    url(r'^geo_user_profile/(?P<username>\w{0,30})/$', user_profile_geolocation, name='user_profile_geolocation'),
#     url(r'^user_profile/$', user_profile),
    url(r'^registered_users/$', RegisteredUsersView.as_view(), name='registered_users_url')
]

admin.site.site_header = 'Handy Man Administration'
