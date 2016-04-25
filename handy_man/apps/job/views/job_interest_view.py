from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.job.models.job import Job
from handy_man.apps.user_profile.models.profile import UserProfile
from handy_man.apps.user_profile.classes import MenuConfiguration


class JobInterestView(BaseDashboard):

    model = Job

    template_name = 'job_posting_interest.html'

    def __init__(self):
        self.context = {}
        self._job_identifier = None
        self._user = None
        self._jobs = []
        super(JobInterestView, self).__init__()

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        self.context.update({
            'latest_jobs': self.latest_jobs,
            'new_jobs': self.jobs_with_job_interest_status,
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        self._job_identifier = request.POST.get('job_id')
        self._user = request.user
        if request.POST.get('action') == 'interested':
            if self.add_job_interest():
                messages.success(request, "Job {} has been allocated to {}".format(self.job, self.user_profile))
            else:
                messages.success(request, "Failed to allocate job to artisan.")
        else:
            if self.cancel_job_interests():
                messages.success(request, "Job Interest log {} has been added successfully.".format(self.job))
            else:
                messages.success(request, "Job Interest log {} has been removed successfully.".format(self.job))
        self.context.update({
            'job_id': self.job.identifier,
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    @property
    def latest_jobs(self):
        return Job.objects.latest_ten_jobs()

    @property
    def all_new_jobs(self):
        return Job.objects.available_jobs()

    @property
    def job(self):
        try:
            job = Job.objects.get(identifier=self._job_identifier)
        except Job.DoesNotExist:
            pass
        return job

    @property
    def job_interest_status(self):
        job_interest_status = Job.objects.filter(
            identifier=self._job_identifier, artisans_interested__in=[self.user_profile])
        return True if job_interest_status else False

    @property
    def jobs_with_job_interest_status(self):
        for job in self.all_new_jobs:
            self._job_identifier = job.identifier
            self._jobs.append([job, self.job_interest_status])
        return self._jobs

    @property
    def user_profile(self):
        try:
            user_profile = UserProfile.objects.get(user__id=self._user_id)
        except UserProfile.DoesNotExist:
            pass
        return user_profile

    def add_job_interest(self):
        if self.job:
            job = self.job
            job.artisans_interested.add(self.user_profile)
            job.save()
            return True
        return False

    def cancel_job_interests(self):
        if self.job:
            job = self.job
            job.artisans_interested.remove(self.user_profile)
            job.save()
            return True
        return False
