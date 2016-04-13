from django.conf.urls import url

from .views import MapGeolocation


urlpatterns = [
    url(r'^map_geolocation/$', MapGeolocation.as_view(), name='map_geolocation_url'),
]
