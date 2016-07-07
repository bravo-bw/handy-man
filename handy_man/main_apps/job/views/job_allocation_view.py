import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http.response import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from handy_man.main_apps.main.views.base_dashboard import BaseDashboard
from handy_man.main_apps.job.models.job import Job
from handy_man.main_apps.user_profile.models.profile import UserProfile
from handy_man.main_apps.user_profile.classes import MenuConfiguration

from handy_man.main_apps.job.classes import JobAllocation


class JobAllocationView(BaseDashboard):

    template_name = 'job_allocation.html'

    def __init__(self):
        self.context = {}
        self._display_single = False
        self._job_identifier = None
        self._user = None
        super(JobAllocationView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JobAllocationView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        self._job_identifier = request.GET.get('job_identifier')
        print ("self._job_identifier", self._job_identifier)
        self._user = request.user
        job_allocation = JobAllocation(self.job, self.user_profile)
        if request.is_ajax():
            if request.GET.get('action') == 'artisan_list':
                data = json.dumps(job_allocation.artisans)
                return HttpResponse(data, content_type='application/json')
            elif request.GET.get('action') == 'assign_job':
                data = None
                if job_allocation.assign_job():
                    message = {'message': "A job has "
                               "been allocated to {} - {}.".format(self._user.first_name, self._user.last_name),
                               "status": "success"}
                    data = json.dumps([message])
                else:
                    message = {'message': "Failed to "
                               "allocated to {} - {}.".format(self._user.first_name, self._user.last_name)}
                    data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
            elif request.GET.get('action') == 're_assign_job':
                data = None
                if job_allocation.cancel_assigned_job():
                    message = {'message': "A job is open for re-assigning.", "status": "success"}
                    data = json.dumps([message])
                else:
                    message = {'message': "Failed to open job for re-assigning.", "status": "failed"}
                    data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
        else:
            page = 1
            self.context.update({
#                 'job_interests': job_allocation.new_jobs_with_job_interest,
                'loggedin_user_profile': loggedin_user_profile,
                'job_interests': Job.objects.all(),
                'task': "job_allocate",
                'artisans': self.paginate_interested_artisans(job_allocation.artisans, page),
                'menus': MenuConfiguration().user_menu_list(self.user_profile)
            })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def paginate_interested_artisans(self, interested_artisans, page):
        paginator = Paginator(interested_artisans, 25)
        try:
            artisans = paginator.page(page)
        except PageNotAnInteger:
            artisans = paginator.page(1)
        except EmptyPage:
            artisans = paginator.page(paginator.num_pages)
        return artisans

    @property
    def job(self):
        try:
            job = Job.objects.get(identifier=self._job_identifier)
        except Job.DoesNotExist:
            job = None
        return job

    @property
    def user_profile(self):
        try:
            user_profile = UserProfile.objects.get(user=self._user)
        except UserProfile.DoesNotExist:
            user_profile = None
        return user_profile
