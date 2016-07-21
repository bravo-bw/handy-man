from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.main_apps.main.views.base_dashboard import BaseDashboard
from handy_man.main_apps.job.models.job import Job
from handy_man.main_apps.user_profile.models.profile import UserProfile
from handy_man.main_apps.user_profile.classes import MenuConfiguration

from handy_man.main_apps.job.classes import JobInterest


class JobInterestView(BaseDashboard):

    model = Job

    template_name = 'job_posting_interest.html'

    def __init__(self):
        self.context = {}
        self._job_identifier = None
        self._user = None
        self._jobs = []
        super(JobInterestView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JobInterestView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        self._job_identifier = request.GET.get('job_identifier')
        self._user = request.user
        job_interest = JobInterest(user_profile=loggedin_user_profile)
        self._user = request.user
        self.context.update({
            'loggedin_user_profile': loggedin_user_profile,
            'latest_jobs': job_interest.latest_jobs,
            'new_jobs': job_interest.new_jobs(),
            'job_identifier': 1,
            'menus': MenuConfiguration().user_menu_list(self.user_profile)
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    @property
    def job(self):
        job = None
        try:
            job = Job.objects.get(identifier=self._job_identifier)
        except Job.DoesNotExist:
            pass
        return job

    @property
    def user_profile(self):
        loggedin_user_profile = None
        try:
            loggedin_user_profile = UserProfile.objects.get(user=self._user)
        except UserProfile.DoesNotExist:
            pass
        return loggedin_user_profile
