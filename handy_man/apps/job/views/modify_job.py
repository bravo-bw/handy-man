import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http.response import HttpResponse

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.main.choices import JOB_STATUS, JOB_TYPE
from handy_man.apps.main.constants import NEW
from handy_man.apps.user_profile.classes import MenuConfiguration
from handy_man.apps.geo_location.models import TownVillage, District, Street
from handy_man.apps.user_profile.views.user_login import  user_profile

from ..forms import JobForm
from ..models import Job, JobType
from handy_man.apps.geo_location.classes import Geolocation


class ModifyJob(BaseDashboard):

    template_name = 'modify_job.html'

    def __init__(self):
        self.context = {}
        super(ModifyJob, self).__init__()

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        job_identifier = kwargs.get('job_identifier')
        job = None
        try:
            job = Job.objects.get(identifier=job_identifier)
        except Job.DoesNotExist:
            pass
        self.context.update({
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile),
            'job': job,
            'status_options': JOB_STATUS
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        job_identifier = kwargs.get('job_identifier')
        job = None
        try:
            job = Job.objects.get(identifier=job_identifier)
        except Job.DoesNotExist:
            pass
        data = {}
        job_form = JobForm
        if request.method == 'POST':
            try:
                job_image_1 = request.POST.get('image1', '')
                job_image_2 = request.POST.get('image2', '')
                job_image_3 = request.POST.get('image3', '')
                status = request.POST.get('job_status', '')
                if job:
                    job.status = status
                    job.save()
                messages.success(request, "Job has been updated successfully")
                return redirect(user_profile, username=loggedin_user_profile.user.username)
            except Exception as err:
                print(err)
        self.context.update({'title': self.title,
                             'job_form': job_form,
                             'job': job,
                             'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)})
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_current_user(self, username):
        try:
            user = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            return None
        return user

    def map_info(self, request):
            data = []
            geo_data = {}
            district = request.GET.get('district')
            town_village = request.GET.get('town_village')
            street = request.GET.get('street')
            geolocation = Geolocation()
            lat, lon = geolocation.cernter_coordinates(district, town_village, street)
            geo_data.update({'latitude': lat, 'longitude': lon})
            if request.GET.get('action') == 'town_village_action':
                data.append(geo_data)
                for street in geolocation.streets(street):
                    data.append(dict({"street": street}))
            elif request.GET.get('action') == 'street_action':
                data.append(geo_data)
            elif request.GET.get('action') == 'district_action':
                district_name = request.GET.get('district')
                town_villages = geolocation.town_villages(district_name)
                data.append(geo_data)
                for town in town_villages:
                    data.append(dict({"town_village": town}))
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')

    @property
    def job_types(self):
        return JobType.objects.all()
