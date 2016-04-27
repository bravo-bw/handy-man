from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.main.choices import JOB_TYPE
from handy_man.apps.main.constants import NEW
from handy_man.apps.user_profile.classes import MenuConfiguration
from handy_man.apps.geo_location.models import TownVillage, District, Street

from ..forms import JobForm
from ..models import Job


class JobPostingView(BaseDashboard):

    template_name = 'job_posting.html'

    def __init__(self):
        self.context = {}
        super(JobPostingView, self).__init__()

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        self.context.update({
            'name': 'Job Posting',
            'job_types': self.job_types,
            'task': "job_post",
            'districts': self.district,
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
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
                    messages.success(request, "Job has been saved successfully")
                except Exception as err:
                    print(err)
        self.context.update({'title': self.title,
                             'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)})
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_current_user(self, username):
        try:
            user = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            return None
        return user

    @property
    def job_types(self):
        job = []
        for x in JOB_TYPE:
            temp = str(x).split(",")
            temp = temp[1].replace(")", "")
            job.append(temp.strip().replace('\'', ''))
        return job

    def streets(self, town_village=None):
        """Return all streets for a town/village."""
        streets = []
#         town_village = TownVillage.objects.all()
        return streets

    def town_village(self, district=None):
        """Return a list of towns."""
        town_village = []
        return town_village

    @property
    def district(self):
        dist = []
        districts = District.objects.all()
        for district in districts:
            dist.append(district.district_name)
        return dist
