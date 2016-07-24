from django.conf.urls import patterns, url
from django.contrib import admin
from .views import Home, ContactUsView

admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.staticfiles.views',
    url(r'^home/', Home.as_view(), name='home_url'),
    url(r'^contact_us', ContactUsView.as_view(), name='contact_us_url')
)
