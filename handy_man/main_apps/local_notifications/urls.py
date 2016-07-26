from django.conf.urls import url

from .views import NotificationView

urlpatterns = [
    url(r'^notifications/', NotificationView.as_view(), name='notifications_url'),
]
