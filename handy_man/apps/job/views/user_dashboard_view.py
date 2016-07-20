from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from handy_man.apps.job.models.job import Job
from datetime import datetime
from handy_man.apps.user_profile.models.profile import UserProfile
from handy_man.apps.user_profile.classes.menu_configuration import MenuConfiguration
from handy_man.apps.main.constants import COMPLETED, ASSIGNED, PENDING, IN_PROGRESS, NEW


class UserDashboardView(TemplateView):

    template_name = 'user_dashboard.html'

    def __init__(self):
        super(UserDashboardView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        context.update(
            job_identifier=self.kwargs.get('job_identifier'),
        )
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        print("<><><><><><><><:self.current_jobs(loggedin_user_profile),", self.current_jobs(loggedin_user_profile),)
        context.update({
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile),
            'completed_jobs': self.completed_jobs(loggedin_user_profile),
            'current_jobs': self.current_jobs(loggedin_user_profile),
        })
        return render(request, self.template_name, context)

    def completed_jobs(self, user_profile):
        return Job.objects.filter(posted_by=user_profile, status=COMPLETED).count()

    def current_jobs(self, user_profile):
        return Job.objects.filter(posted_by=user_profile, status__in=[ASSIGNED, PENDING, IN_PROGRESS, NEW]).count()
