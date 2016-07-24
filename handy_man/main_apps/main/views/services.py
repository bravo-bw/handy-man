from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from handy_man.main_apps.user_profile.classes.menu_configuration import MenuConfiguration
from handy_man.main_apps.user_profile.models.profile import UserProfile


class ServicesView(TemplateView):

    template_name = 'services.html'

    def __init__(self):
        super(ServicesView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServicesView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        context.update({
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
        })
        return render(request, self.template_name, context)
