from django.contrib import messages 
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.job.models.job import Job
from handy_man.apps.user_profile.models.profile import UserProfile


class JobAllocationView(BaseDashboard):

    template_name = 'job_allocation.html'

    def __init__(self):
        self.context = {}
        self._job_identifier = None
        super(JobAllocationView, self).__init__()

    def get(self, request, *args, **kwargs):
        self.context.update({
            'name': 'Setsiba',
            'task': "job_allocate"
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self._job_identifier = request.POST.get('job_id')
        self._user_id = request.POST.get('artisan')
        messages.success(request, "Job {} has been allocated to {}")
        if self.assign_job():
            messages.success(request, "Job {} has been allocated to {}".format(self.job, self.user_profile))
        else:
            messages.success(request, "Failed to allocate job to artisan.")
        self.context.update({
            'title': self.title,
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    @property
    def job(self):
        try:
            job = Job.objects.get(identifier=self._job_identifier)
        except Job.DoesNotExist:
            pass
        return job

    @property
    def user_profile(self):
        try:
            user_profile = UserProfile.objects.get(user__id=self._user_id)
        except UserProfile.DoesNotExist:
            pass
        return user_profile

    def assign_job(self):
        if self.job:
            job = self.job
            job.allocated_to = self.user_profile
            job.save()
            return True
        return False

    def job_cancel(self):
        pass
