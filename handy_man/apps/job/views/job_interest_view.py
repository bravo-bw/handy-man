import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponse

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.job.models.job import Job
from handy_man.apps.user_profile.models.profile import UserProfile
from handy_man.apps.user_profile.classes import MenuConfiguration

from ..classes import JobInterest


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
        job_interest = JobInterest(self.job, self.user_profile)
        if request.is_ajax():
            self._user = request.user
            self._job_identifier = request.GET.get('job_identifier')
            if request.GET.get('action') == 'add_job_interest':
                if job_interest.add_job_interest():
                    message = {'message': "Job request has been submitted.", "status": "success"}
                    data = json.dumps([message])
                else:
                    message = {'message': "Failed to submit job request.", "status": "failed"}
                    data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
            elif request.GET.get('action') == 'cancel_job_interest':
                data = None
                if job_interest.cancel_job_interests():
                    message = {'message': "Job request for has been cancelled.", "status": "success"}
                    data = json.dumps([message])
                else:
                    message = {'message': "Failed to cancel job request.", "status": "failed"}
                    data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
        else:
            self._user = request.user
            self.context.update({
                'latest_jobs': job_interest.latest_jobs,
                'new_jobs': job_interest.jobs_with_job_interest_status,
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
