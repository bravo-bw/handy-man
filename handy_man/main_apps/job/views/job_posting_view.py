import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http.response import HttpResponse

from handy_man.main_apps.main.views.base_dashboard import BaseDashboard
from handy_man.main_apps.user_profile.models import UserProfile
from handy_man.main_apps.user_profile.views.user_login import user_profile
from handy_man.main_apps.user_profile.classes import MenuConfiguration
from handy_man.main_apps.geo_location.models import TownVillage, District, Street

from handy_man.main_apps.job.forms import JobForm
from handy_man.main_apps.job.models import JobType
from handy_man.main_apps.geo_location.classes import Geolocation


class JobPostingView(BaseDashboard):

    template_name = 'job_posting.html'

    def __init__(self):
        self.context = {}
        super(JobPostingView, self).__init__()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.map_info(request)
        else:
            loggedin_user_profile = UserProfile.objects.get(user=request.user)
            geolocation = Geolocation()
            district_name = request.GET.get('district_name', '')
            town_village_name = request.GET.get('town_village_name', '')
            street_name = request.GET.get('street_name', '')
            self.context.update({
                'name': 'Job Posting',
                'job_types': self.job_types,
                'task': "job_post",
                'districts': geolocation.districts,
                'town_villages': geolocation.town_villages(district_name),
                'district_name': district_name,
                'town_village_name': town_village_name,
                'street_name': street_name,
                'coordinates': geolocation.cernter_coordinates(district_name, town_village_name, street_name),
                'streets': geolocation.streets(town_village_name),
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
            return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        posted_by = self.get_current_user(request.user.username)
        data = {}
        job_form = JobForm
        if request.method == 'POST':
            try:
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                district_name = request.POST.get('district_select')
                street_name = request.POST.get('street_select')
                town_village_name = request.POST.get('town_village_select')
                description = request.POST.get('description')
                job_image_1 = request.POST.get('image1', '')
                job_image_2 = request.POST.get('image2', '')
                job_image_3 = request.POST.get('image3', '')
                try:
                    job_type = JobType.objects.get(pk=request.POST.get('job_type'))
                except JobType.DoesNotExist:
                    job_type = None
                except:
                    print(request.POST.get('job_type'))
                street = None
                district = None
                town_village = None
                try:
                    district = District.objects.get(district_name=district_name)
                except District.DoesNotExist:
                    pass
                try:
                    town_village = TownVillage.objects.get(town_village_name=town_village_name)
                except TownVillage.DoesNotExist:
                    pass
                try:
                    street = Street.objects.get(street_name=street_name)
                except Street.DoesNotExist:
                    pass
                data = {'latitude': latitude, 'longitude': longitude, 'district': district.id, 'town_village': town_village.id,
                        'posted_by': posted_by.id, 'street': street.id, 'description': description, 'job_image_1': job_image_1,
                        'job_image_2': job_image_2, 'job_image_3': job_image_3, 'job_type': job_type.id}
                job_form = JobForm(data)
                if job_form.is_valid():
                    job_form.save()
                else:
                    pass
#                     Job.objects.create(
#                         posted_by=posted_by, latitude=latitude, longitude=longitude, district=district, street=street, job_type=job_type,
#                         town_village=town_village, status=NEW, description=description,
#                         job_image_1=job_image_1, job_image_2=job_image_2, job_image_3=job_image_3)
                messages.success(request, "Job has been saved successfully")
                return redirect(user_profile, username=loggedin_user_profile.user.username)
            except Exception as err:
                print(err)
                print(job_form.errors)
        self.context.update({'title': self.title,
                             'job_form': job_form,
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
