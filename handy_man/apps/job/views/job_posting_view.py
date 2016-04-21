from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages 

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.main.choices import JOB_STATUS, JOB_TYPE
from handy_man.apps.main.constants import NEW
from ..forms import JobForm
from ..models import Job


class JobPostingView(BaseDashboard):

    template_name = 'job_posting.html'

    def __init__(self):
        self.context = {
            'job_type': JOB_TYPE,
        }
        super(JobPostingView, self).__init__()

    def get(self, request, *args, **kwargs):
        self.context.update({
            'name': 'Job Posting View',
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        posted_by = self.get_current_user(request.user.username)
        job_posting_form = JobForm(request.POST)
        if request.method == 'POST':
            if job_posting_form.is_valid():
                try:
                    latitude = request.POST.get('latitude')
                    longitude = request.POST.get('longitude')
                    street = request.POST.get('street')
                    town_village = request.POST.get('town_village')
                    description = request.POST.get('description')
                    job_type = request.POST.get('job_type')
                    job_image_1 = request.POST.get('job_image_1', '')
                    job_image_2 = request.POST.get('job_image_2', '')
                    job_image_3 = request.POST.get('job_image_3', '')
                    job = Job.objects.create(
                        posted_by=posted_by, latitude=latitude, longitude=longitude, street=street, job_type=job_type,
                        town_village=town_village, status=NEW, description=description,
                        job_image_1=job_image_1, job_image_2=job_image_2, job_image_3=job_image_3)
                    job.save()
                except Exception as err:
                    print(err)
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_current_user(self, username):
        try:
            user = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            return None
        return user
