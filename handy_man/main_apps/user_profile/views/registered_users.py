from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from handy_man.main_apps.main.views import BaseDashboard
from handy_man.main_apps.user_profile.models import UserProfile

from handy_man.main_apps.user_profile.classes import MenuConfiguration


class RegisteredUsersView(BaseDashboard):
    def __init__(self):
        self.context = {}
        self.template_name = 'registered_users.html'
        super(RegisteredUsersView, self).__init__()

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        if request.user.is_authenticated():
            results = UserProfile.objects.filter(email_validated=True, administrator_validated=True)
            self.context.update({
                'user_profiles': results,
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        else:
            return redirect('/login')
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        return redirect('/login')

    def get_context_data(self, **kwargs):
        return super(RegisteredUsersView, self).get_context_data(**kwargs)
