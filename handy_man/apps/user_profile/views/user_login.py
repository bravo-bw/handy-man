import json
import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import HttpResponse

from updown.models import SCORE_TYPES

from handy_man.apps.main.constants import IN_PROGRESS, COMPLETED, NEW, ARTISAN, CUSTOMER
from handy_man.apps.job.models import Job
from handy_man.apps.user_profile.models import UserProfile, Profession
from handy_man.apps.user_profile.forms import (AuthenticateForm, UserCreateForm, UserProfileForm)
from handy_man.apps.geo_location.classes import Geolocation

from ..classes import MenuConfiguration
from handy_man.apps.job.models.job_type import JobType
from handy_man.apps.job.classes.job_helper import JobHelper


def get_latest(user):
    try:
        return user.ribbit_set.order_by('-id')[0]
    except IndexError:
        return ""


@login_required
def user_profile(request, username):
    loggedin_user_profile = UserProfile.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user__username=username)
    if user_profile.account_type == ARTISAN:
        user_jobs = Job.objects.filter(allocated_to=user_profile)
    elif user_profile.account_type == CUSTOMER:
        user_jobs = Job.objects.filter(posted_by=user_profile)
    else:
        user_jobs = Job.objects.filter(posted_by=user_profile)
    user_current_jobs = user_jobs.filter(status__in=[IN_PROGRESS, NEW])
    like = request.GET.get('score_type', '')
    job_identifier = request.GET.get('job_identifier', '')
    job = None
    if job_identifier:
        try:
            job = Job.objects.get(identifier=job_identifier)
            job.rating.add(SCORE_TYPES[like], loggedin_user_profile.user, request.META['REMOTE_ADDR'])
        except Job.DoesNotExist:
            pass
    user_completed_jobs = user_jobs.filter(status=COMPLETED)
    geolocation = Geolocation()
    district_name = request.GET.get('district_name', '')
    town_village_name = request.GET.get('town_village_name', '')
    street_name = request.GET.get('street_name', '')
    if request.is_ajax():
        if request.GET.get('action') == 'save_job_changes':
            job_id = request.GET.get('job_identifier')
            description = request.GET.get('description')
            job_closing_date = request.GET.get('job_closing_date') or None
            if job_closing_date:
                job_closing_date = datetime.datetime.strptime(job_closing_date, '%d/%m/%Y').date()
            print ("Job closing date:", job_closing_date)
            job_type = request.GET.get('job_type')
            status, message = save_job_changes(job_id, description, job_type, job_closing_date)
            data = None
            if status:
                msg = {'message': message}
                data = json.dumps(msg)
            else:
                msg = {'message': message}
                data = json.dumps(msg)
            return HttpResponse(data, content_type='application/json')
    elif request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                avatar_image = request.FILES['avatar_image']
                user_profile.avatar_image = avatar_image
                user_profile.save()
            except MultiValueDictKeyError:
                pass
            except Exception as e:
                raise e
            updated_user_values = {}
            updated_profile_values = {}
            for fld in UserProfileForm.Meta.fields:
                updated_user_values[fld] = form.cleaned_data.get(fld)
            for fld in UserProfileForm.Meta.profile_fields:
                updated_profile_values[fld] = form.cleaned_data.get(fld)
            User.objects.filter(id=request.user.id).update(**updated_user_values)
            #updated_profile_values['avatar_image'] = avatar_image
            UserProfile.objects.filter(user=request.user).update(**updated_profile_values)
            return HttpResponseRedirect('/profile/user_profile/{}/'.format(user_profile.user.username))
    else:
        # If requet is a get, then do just display profile values.
        pass
#         form_values = {}
#         for fld in UserProfileForm.Meta.fields:
#             form_values[fld] = user_profile.user.__dict__[fld]
#         for fld in UserProfileForm.Meta.profile_fields:
#             print user_profile.__dict__[fld]
#             form_values[fld] = user_profile.__dict__[fld]
#         form = UserProfileForm(form_values)
#         print form.instance.__dict__

    return render(request,
                  'user_profile.html',
                  {'user_profile': user_profile,
                   'districts': geolocation.districts,
                   'professions': Profession.objects.all(),
                   'town_villages': geolocation.town_villages(district_name),
                   'district_name': district_name,
                   'town_village_name': town_village_name,
                   'street_name': street_name,
                   'coordinates': geolocation.cernter_coordinates(district_name, town_village_name, street_name),
                   'streets': geolocation.streets(town_village_name),
                   'logged_in_user': request.user,
                   'user_current_jobs': user_current_jobs,
                   'user_completed_jobs': user_completed_jobs,
                   'job_types': JobType.objects.all(),
                   'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)})


@login_required
def user_profile_documents(request, username):
    loggedin_user_profile = UserProfile.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user__username=username)
    if request.method == 'POST':
        count = 1
        user_profile.document_1 = None
        user_profile.document_2 = None
        user_profile.document_3 = None
        try:
            for value in request.FILES.getlist('input-24'):
                setattr(user_profile, 'document_{}'.format(count), value)
                count += 1
            user_profile.save()
        except MultiValueDictKeyError:
            pass
        except Exception as e:
            raise e
        return HttpResponseRedirect('/profile/user_profile/{}/'.format(user_profile.user.username))
    else:
        # If requet is a get, then do just display profile values.
        pass

    return render(request,
                  'user_profile.html',
                  {'user_profile': user_profile,
                   'logged_in_user': request.user,
                   'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)})


def index(request, auth_form=None, user_form=None):

    if request.user.is_authenticated():

        user = request.user
        model = ''

        return render(request,
                      'buddies.html',
                      {
                       'user': user,
                       'model': model,
                       'registration': [],
                       'sighting_type': [],
                       'notifications': [],
                       'public_notifications': [],
                       'next_url': '/',
                       'username': request.user.username,  })
    else:
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('form-username', '')
        password = request.POST.get('form-password', '')
        data = {'username': username, 'password': password}
        print(data, "**&&login dict")
        form = AuthenticateForm(data=data)
        user_profile = UserProfile.objects.filter(user__username=username, email_validated=True)
        if form.is_valid() and user_profile:
            login(request, form.get_user())

#             if user_profile[0].account == SHIPPER:
#                 return redirect('/shipper?job_type=my_jobs')
#             else:
#                 return redirect('/goods_owner/1')
        else:
            return index(request, auth_form=form)
    return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def verify_account(request, username):
    try:
        user_profile = UserProfile.objects.get(user__username=username)
        user_profile.email_validated = True
        user_profile.save()
        message = "Congratulations '{}', your EMAIL has been verified.".format(user_profile.user.first_name)
    except UserProfile.DoesNotExist:
        message = "The username '{}' does not exist in the system. Please register first.".format(username)
    return render(request,
                    'verify.html',
                    {'message': message
                     })


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('form-email', '')
        first_name = request.POST.get('form-first-name', '')
        last_name = request.POST.get('form-last-name', '')
        mobile = request.POST.get('form-mobile', '')
        username = request.POST.get('form-username', '')
        password1 = request.POST.get('form-password1', '')
        password2 = request.POST.get('form-password2', '')
        account_type = request.POST.get('form-account_type', '')
        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'mobile': mobile,
            'username': username,
            'password1': password1,
            'password2': password2,
            'account_type': account_type}
        user_form = UserCreateForm(data=data)
        if user_form.is_valid():
            with transaction.atomic():
                user_form.save()
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
                user = user_form.instance
                form_values = {}
                for fld in UserCreateForm.Meta.profile_fields:
                    form_values[fld] = user_form.cleaned_data[fld]
                form_values['user'] = user
                UserProfile.objects.create(**form_values)
                subject = "verify account (BW Handy Man portal)"
                body = 'Thank you for registering with BW Handy Man ' \
                        'click the following link to verify your EMAIL.' \
                        ' http://localhost:8000/profile/verify/{}'.format(user.username)
                email_sender = settings.EMAIL
                recipient_list = [user.email, ]
                send_mail(subject, body, email_sender, recipient_list, fail_silently=False)
                return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')


@login_required
def user_profile_geolocation(request, username):
    loggedin_user_profile = UserProfile.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user__username=username)
    user_jobs = Job.objects.filter(allocated_to=user_profile)
    user_current_jobs = user_jobs.filter(status__in=[IN_PROGRESS, NEW])
    user_completed_jobs = user_jobs.filter(status=COMPLETED)
    geolocation = Geolocation()
    district_name = request.GET.get('district_name', '')
    town_village_name = request.GET.get('town_village_name', '')
    street_name = request.GET.get('street_name', '')
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                avatar_image = request.FILES['avatar_image']
                user_profile.avatar_image = avatar_image
                user_profile.save()
            except MultiValueDictKeyError:
                pass
            except Exception as e:
                raise e
            updated_user_values = {}
            updated_profile_values = {}
            for fld in UserProfileForm.Meta.fields:
                updated_user_values[fld] = form.cleaned_data.get(fld)
            for fld in UserProfileForm.Meta.profile_fields:
                updated_profile_values[fld] = form.cleaned_data.get(fld)
            User.objects.filter(id=request.user.id).update(**updated_user_values)
            #updated_profile_values['avatar_image'] = avatar_image
            UserProfile.objects.filter(user=request.user).update(**updated_profile_values)
            return HttpResponseRedirect('/profile/user_profile/{}/'.format(user_profile.user.username))
    else:
        # If requet is a get, then do just display profile values.
        pass
#         form_values = {}
#         for fld in UserProfileForm.Meta.fields:
#             form_values[fld] = user_profile.user.__dict__[fld]
#         for fld in UserProfileForm.Meta.profile_fields:
#             print user_profile.__dict__[fld]
#             form_values[fld] = user_profile.__dict__[fld]
#         form = UserProfileForm(form_values)
#         print form.instance.__dict__

    return render(request,
                  'user_profile.html',
                  {'user_profile': user_profile,
                   'districts': geolocation.districts,
                   'town_villages': geolocation.town_villages(district_name),
                   'district_name': district_name,
                   'town_village_name': town_village_name,
                   'street_name': street_name,
                   'coordinates': geolocation.cernter_coordinates(district_name, town_village_name, street_name),
                   'streets': geolocation.streets(town_village_name),
                   'logged_in_user': request.user,
                   'user_current_jobs': user_current_jobs,
                   'user_completed_jobs': user_completed_jobs,
                   'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)})


def save_job_changes(job_id, description, jotype, est):
    """
        1. check whether the job can be changed.
        2. if job can be changed then save
        3. On post save then notify artisans who have logged interest for the job.
    """
    try:
        job = Job.objects.get(identifier=job_id)
        jtype = job_type(jotype) if job_type(jotype) else None
        job_helper = JobHelper(job=job, job_type=jtype, estimated_job_closing_date=est)
        if job_helper.save_job():
            return (True, "Job has been updated successfully.")
        else:
            if job_helper.validate_job_change:
                return (False, "Assigned job or completed cannot be modified.")
    except Job.DoesNotExist:
        return (False, "Cannot find job record, failed to update.")
    return (False, "Failed to update job")


def job_type(job_type):
    try:
        joype = JobType.objects.get(id=job_type)
    except JobType.DoesNotExist:
        return False
    return joype

