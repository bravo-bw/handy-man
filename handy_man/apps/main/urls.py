from django.conf.urls import patterns, url
from django.contrib import admin
from .views import Home

admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
    url(r'^home/', Home.as_view(), name='home_url'),
)
