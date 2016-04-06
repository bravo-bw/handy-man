from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from code_rumble.apps.main.views.user_login import (user_profile, users, login_view, signup, logout_view,
                                                    verify_account)

from code_rumble.apps.main.views import Shipper, AddBid, ViewBids, create_get, ViewNotifications
from code_rumble.apps.main.views import Shipper, create_get, GoodsOwner, AccountDetails


from .views import Home

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Home.as_view(), name='home_url'),
#     url(r'^login$', login_view),
#     url(r'^logout$', logout_view),
#     url(r'^signup$', signup),
#     url(r'^users/$', users),
#     url(r'^verify/(?P<username>\w{0,30})$', verify_account),
#     url(r'^users/(?P<username>\w{0,30})/$', users),
#     url(r'^user_profile/(?P<username>\w{0,30})/$', user_profile, name='user_profile'),
#     url(r'^user_profile/$', user_profile),
    url(r'shipper$', login_required(Shipper.as_view()), name='shipper_url'),
    url(r'add_bid', login_required(AddBid.as_view()), name='submit_bid_url'),
    url(r'view_bids', login_required(ViewBids.as_view()), name='view_bids_url'),
    url(r'^goods_owner/(?P<task_id>[1-9]{1})$', login_required(login_required(GoodsOwner.as_view())), name='goods_owner_url'),
    url(r'^view_notifications', login_required(ViewNotifications.as_view()), name='view_notifications'),
    url(r'^job', create_get, name='job_url'),
    url(r'^account_details/(?P<username>\w{0,30})/$', login_required(AccountDetails.as_view()), name='banking_url')
)

urlpatterns += patterns(
    'django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
