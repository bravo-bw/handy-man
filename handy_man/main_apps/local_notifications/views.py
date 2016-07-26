from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext

from notifications.models import Notification

from handy_man.main_apps.main.views.base_dashboard import BaseDashboard
from handy_man.main_apps.user_profile.models.profile import UserProfile
from handy_man.main_apps.user_profile.classes import MenuConfiguration


class NotificationView(BaseDashboard):

    template_name = 'local_notifications.html'

    def __init__(self):
        self.context = {}
        self._display_single = False
        self._job_identifier = None
        self._user = None
        super(NotificationView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotificationView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        notifications = Notification.objects.all()
        notifications_count = notifications.count()
        self._user = request.user
        self.context.update({
            'notifications': notifications,
            'loggedin_user_profile': loggedin_user_profile,
            'notifications_count': notifications_count,
            'menus': MenuConfiguration().user_menu_list(self.user_profile)
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    @property
    def user_profile(self):
        try:
            user_profile = UserProfile.objects.get(user=self._user)
        except UserProfile.DoesNotExist:
            user_profile = None
        return user_profile
