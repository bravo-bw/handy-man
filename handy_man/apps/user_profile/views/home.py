from django.shortcuts import render_to_response
from django.template import RequestContext
from .base_dashboard import BaseDashboard
from ..forms import AuthenticateForm, UserCreateForm


class Home(BaseDashboard):

    def __init__(self):
        self.context = {}
        self.template_name = 'home.html'
        super(Home, self).__init__()

    def get(self, request, *args, **kwargs):
        notifications = 'Notifications.objects.all()'
        if request.user.is_authenticated():
            user = request.user
            model = ''
            self.context.update({
                'title': self.title,
                'notifications': notifications,
                'user': user,
                'model': model,
                'registration': [],
                'sighting_type': [],
                'notifications': [],
                'public_notifications': [],
                'next_url': '/',
                'username': request.user.username,
            })
        else:
            auth_form = AuthenticateForm()
            user_form = UserCreateForm()
            self.context.update({
                'title': self.title,
                'notifications': notifications,
                'auth_form': auth_form,
                'user_form': user_form,
            })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
            'title': self.title
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):

        return super(Home, self).get_context_data(**kwargs)
