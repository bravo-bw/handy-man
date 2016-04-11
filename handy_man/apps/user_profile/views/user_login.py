from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError

from handy_man.apps.main.constants import SHIPPER
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.user_profile.forms import (AuthenticateForm, UserCreateForm, UserProfileForm)


def get_latest(user):
    try:
        return user.ribbit_set.order_by('-id')[0]
    except IndexError:
        return ""


@login_required
def users(request, username="", ribbit_form=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        ribbits = Ribbit.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            return render(request, 'user.html', {'user': user, 'ribbits': ribbits, })
        return render(request, 'user.html', {'user': user, 'ribbits': ribbits, 'follow': True, })
    users = User.objects.all().annotate(ribbit_count=Count('ribbit'))
    ribbits = map(get_latest, users)
    obj = zip(users, ribbits)
    ribbit_form = ribbit_form or LeoForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'ribbit_form': ribbit_form,
                   'username': request.user.username, })


@login_required
def user_profile(request, username=None):
    user_profile = UserProfile.objects.get(user=request.user)
    user = user_profile.user
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
                   'user': user})


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
        form = AuthenticateForm(data=request.POST)
        user_profile = UserProfile.objects.filter(user__username=request.POST.get('username'), email_validated=True)
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
        user_profile.validated = True
        user_profile.save()
        message = "Congratulations '{}', your account has been verified.".format(user_profile.user.first_name)
    except UserProfile.DoesNotExist:
        message = "The username '{}' does not exist in the system. Please register first.".format(username)
    return render(request,
                    'verify.html',
                    {'message': message
                     })


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
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
                subject = "verify account (BW shipping portal)"
                body = 'Thank you for registering with BW shipping portal ' \
                        'click the following link to verify your email.' \
                        'http://localhost:8000/verify/{}'.format(user.username)
                email_sender = "coderumble2016@gmail.com"
                recipient_list = [user.email, ]
                send_mail(subject, body, email_sender, recipient_list, fail_silently=False)
                return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')
