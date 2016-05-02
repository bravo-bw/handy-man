from django.shortcuts import render_to_response
from django.template import RequestContext
from handy_man.apps.main.views import BaseDashboard
from handy_man.apps.user_profile.forms import AuthenticateForm, UserCreateForm
from handy_man.apps.user_profile.models.profile import UserProfile
from handy_man.apps.user_profile.classes import MenuConfiguration


class Home(BaseDashboard):

    def __init__(self):
        self.context = {}
        self.template_name = 'home.html'
        super(Home, self).__init__()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            loggedin_user_profile = UserProfile.objects.get(user=request.user)
            user = request.user
            model = ''
            self.context.update({
                'title': self.title,
                'user': user,
                'model': model,
                'registration': [],
                'sighting_type': [],
                'notifications': [],
                'public_notifications': [],
                'next_url': '/',
                'username': request.user.username,
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        else:
            auth_form = AuthenticateForm()
            user_form = UserCreateForm()
            self.context.update({
                'title': self.title,
                'auth_form': auth_form,
                'user_form': user_form,
            })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        self.context.update({
            'title': self.title,
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):

        return super(Home, self).get_context_data(**kwargs)
