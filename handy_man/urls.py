from django.contrib.staticfiles.views import serve
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.generic import RedirectView
from handy_man.main_apps.user_profile.views import (login_view, signup, logout_view)
from handy_man.main_apps.main.views import Home
from handy_man.main_apps.main.views import SearchView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name='handy_man'))),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', Home.as_view(), name='home_url'),
    url(r'^login$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^handy_man/logout/$', logout_view),
    url(r'^search$', SearchView.as_view(), name='search_url_get'),
    url(r'^signup$', signup),
    url(r'^profile/', include('handy_man.main_apps.user_profile.urls')),
    url(r'^jobs/', include('handy_man.main_apps.job.urls')),
    url(r"^notifications/", include("pinax.notifications.urls")),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]


urlpatterns += patterns(
    url(r'^static/(?P<path>.*)$', serve),
)
