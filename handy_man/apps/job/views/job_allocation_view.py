import json

from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.job.models.job import Job
from django.http.response import HttpResponse
from handy_man.apps.user_profile.models.profile import UserProfile


class JobAllocationView(BaseDashboard):

    template_name = 'job_allocation.html'

    def __init__(self):
        self.context = {}
        self._display_single = False
        self._job_identifier = None
        super(JobAllocationView, self).__init__()

    def get(self, request, *args, **kwargs):
        self._job_identifier = request.GET.get('job_id')
        if request.is_ajax():
            if request.GET.get('action') == 'artisan_list':
                return self.job_artisans(request)
            elif request.GET.get('action') == 'assign_job':
                data = None
                if self.assign_job():
                    message = {'message': "A job has been allocated to Tshepiso Setsiba."}
                    data = json.dumps([message])
                else:
                    message = {'message': "Failed to allocated to Tshepiso Setsiba."}
                    data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
            elif request.GET.get('action') == 're_assign_job':
                data = None
                if self.cancel_assigned_job():
                    message = {'message': "A job is open for re-assigning."}
                    data = json.dumps([message])
                else:
                    message = {'message': "Failed to open job for re-assigning.", "status": "success"}
                    data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
        else:
            self._display_single = True if request.GET.get('display_mode') == "single" else False
            job_interests = []
            if self._display_single:
                job_interests.append(self.job)
            else:
                job_interests = self.new_jobs_with_job_interest
            self.context.update({
                'job_interests': job_interests,
                'task': "job_allocate",
                'artisans': self.artisans
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
            job = None
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

    def cancel_assigned_job(self):
        job = self.job
        is_cancelled = False
        if job:
            job.allocated_to = None
            job.save()
            is_cancelled = True
        return is_cancelled

    @property
    def artisans(self):
        artisans = []
        job = self.job
        if job:
            for artisan in job.artisans_interested.all():
                temp = {}
                temp.update({'artisan_id': artisan.id,
                             'username': artisan.user.username,
                             'full_name': "{} - {}".format(artisan.user.first_name, artisan.user.last_name),
                             'avatar': artisan.avatar_image,
                             'job_identifier': job.identifier})
                artisans.append(temp)
        return artisans

    @property
    def new_jobs_with_job_interest(self):
        new_jobs_with_job_interest = []
        for job in Job.objects.filter(status__in=['new', 'assigned']):
            if job.artisans_interested.all():
                new_jobs_with_job_interest.append(job)
        return new_jobs_with_job_interest

    def job_artisans(self, request):
        data = json.dumps(self.artisans)
        return HttpResponse(data, content_type='application/json')
