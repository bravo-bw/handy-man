from django.conf.urls import patterns, url
from django.contrib import admin
<<<<<<< HEAD
from .views import Home

admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.staticfiles.views',
    url(r'^home/', Home.as_view(), name='home_url'),
)
=======
from django.contrib.auth.decorators import login_required

from handy_man.apps.user_profile.views import Home
# from handy_man.apps.main.views import Shipper, AddBid, ViewBids, create_get, ViewNotifications
# from handy_man.apps.main.views import Shipper, create_get, GoodsOwner, AccountDetails

urlpatterns = [
    '',
    url(r'^$', Home.as_view(), name='home_url'),
#     url(r'^login$', login_view),
#     url(r'^logout$', logout_view),
#     url(r'^signup$', signup),
#     url(r'^users/$', users),
#     url(r'^verify/(?P<username>\w{0,30})$', verify_account),
#     url(r'^users/(?P<username>\w{0,30})/$', users),
#     url(r'^user_profile/(?P<username>\w{0,30})/$', user_profile, name='user_profile'),
#     url(r'^user_profile/$', user_profile),
#     url(r'shipper$', login_required(Shipper.as_view()), name='shipper_url'),
#     url(r'add_bid', login_required(AddBid.as_view()), name='submit_bid_url'),
#     url(r'view_bids', login_required(ViewBids.as_view()), name='view_bids_url'),
#     url(r'^goods_owner/(?P<task_id>[1-9]{1})$', login_required(login_required(GoodsOwner.as_view())), name='goods_owner_url'),
#     url(r'^view_notifications', login_required(ViewNotifications.as_view()), name='view_notifications'),
#     url(r'^job', create_get, name='job_url'),
#     url(r'^account_details/(?P<username>\w{0,30})/$', login_required(AccountDetails.as_view()), name='banking_url')
]
>>>>>>> 13cb60542f84e50a45662ddca15aeba982aea898
