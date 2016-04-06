from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from handy_man.apps.user_profile.views import (login_view, signup, logout_view, Home)

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name='handy_man'))),
    (r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns(
    '',
    url(r'^$', Home.as_view(), name='home_url'),
    url(r'^login$', login_view),
    url(r'^logout$', logout_view),
    url(r'^signup$', signup),
    (r'^profile/', include('handy_man.apps.user_profile.urls')),
#     (r'^main/', include('handy_man.apps.main.urls')),
)

urlpatterns += patterns(
    'django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)

urlpatterns += staticfiles_urlpatterns()
