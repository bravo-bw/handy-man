import json

from django.views.generic import View
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, RequestContext
from .base_dashboard import BaseDashboard

from ..models import Job, UserProfile
from ..constants import NEW, IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED


class AddBid(BaseDashboard):

    def __init__(self):
        self.context = {}
        self.template_name = 'shipper.html'
        super(AddBid, self).__init__()

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        job = Job.objects.get(job_identifier=request.POST.get('job_identifier'))
        amount = request.POST.get('amount')
        user_profile = UserProfile.objects.get(user__username=request.user.username)
        user_profile.submit_bid(job, amount)
        public_jobs = Job.objects.filter(job_status__in=[NEW])
        my_jobs = Job.objects.filter(job_status__in=[IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED],
                                     exercutor__user__username=request.user.username)
        if request.POST.get('job_type') == 'available_jobs':
            self.template_name = "shipper_available_jobs.html"
        else:
            self.template_name = "shipper.html"
        self.context.update({
            'title': self.title,
            'public_jobs': public_jobs,
            'my_jobs': my_jobs,
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))