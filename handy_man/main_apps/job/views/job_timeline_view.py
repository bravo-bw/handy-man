from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from handy_man.main_apps.job.models.job import Job
from handy_man.main_apps.job.models.quote import Quote
from datetime import datetime
from handy_man.main_apps.user_profile.models.profile import UserProfile
from handy_man.main_apps.user_profile.classes.menu_configuration import MenuConfiguration


class JobTimelineView(TemplateView):

    template_name = 'job_timeline.html'

    def __init__(self):
        super(JobTimelineView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JobTimelineView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobTimelineView, self).get_context_data(**kwargs)
        context.update(
            job_identifier=self.kwargs.get('job_identifier'),
        )
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        job_identifier = context.get('job_identifier')
        job_identifier = int(job_identifier.split('/')[0])
        job = self.job(job_identifier)
        context.update(self.assigned_artisan(job_identifier))
        context.update(self.posted_by(job_identifier))
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        context.update({
            'job': job,
            'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
        })
        return render(request, self.template_name, context)

    def assigned_artisan(self, job_identifier):
        assigned_artisan = {}
        job = self.job(job_identifier)
        if job.allocated_to:
            assigned_artisan.update({
                'assigned_artisan_avatar': '/static/{}'.format(str(job.allocated_to.avatar_image).split('/')[-1]),
                'assigned_artisan_fullname': '{} - {}'.format(job.allocated_to.user.first_name, job.allocated_to.user.last_name),
                'profession': job.allocated_to.profession if job.allocated_to.profession else 'Profession Not Specified',
                'about': "Work on cutting edge technology >>Do what everyone is doing. Must be a team player >> Must not question authority."
            })
        else:
            assigned_artisan.update({
                'assigned_artisan_avatar': '/static/gfx/default_avatar_male.jpg',
                'assigned_artisan_fullname': 'Not Assigned',
                'profession': 'NA',
                'about': 'Work on cutting edge technology'
            })
        return assigned_artisan

    def posted_by(self, job_identifier):
        posted_by = {}
        job = self.job(job_identifier)
        job_has_completed = True if job.status == 'completed' else False
        quote = self.job_quotations(job)
        artisan_full_name = quote.artisan.user.get_full_name() if quote else False
        posted_by.update({
            'posted_by_avatar': '/static/{}'.format(str(job.posted_by.avatar_image).split('/')[-1]),
            'posted_by_fullname': '{}'.format(job.posted_by.user.get_full_name()),
            'posted_by_profession': job.posted_by.profession if job.posted_by.profession else 'Profession Not Specified',
            'posted_by_about': "N/A",
            'job_completed_by_fullname': self.job_completed_by_fullname(quote),
            'job_has_completed': job_has_completed,
            'username': job.posted_by.user.username,
            'quote': quote,
            'artisan_full_name': artisan_full_name,
            'today_date': datetime.today()
        })
        return posted_by

    def job(self, job_identifier):
        try:
            return Job.objects.get(identifier=job_identifier)
        except Job.DoesNotExist:
            return False

    def job_quotations(self, job):
        try:
            quote = Quote.objects.get(accepted=True, job=job)
        except Quote.DoesNotExist:
            return False
        return quote

    def job_completed_by_fullname(self, quote):
        if quote:
            return '{}'.format(quote.artisan.user.first_name, quote.artisan.user.last_name)
        else:
            return ''
