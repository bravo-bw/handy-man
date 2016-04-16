from django.conf.urls import patterns, url
from django.contrib import admin
from handy_man.apps.user_profile.views import Home

admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
    url(r'^home/', Home.as_view(), name='home_url'),
)
