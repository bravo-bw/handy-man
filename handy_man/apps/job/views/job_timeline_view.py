from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from handy_man.apps.job.models.job import Job


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
        context.update({
            'job': job,
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
        posted_by.update({
            'posted_by_avatar': '/static/{}'.format(str(job.posted_by.avatar_image).split('/')[-1]),
            'posted_by_fullname': '{} - {}'.format(job.posted_by.user.first_name, job.posted_by.user.last_name),
            'posted_by_profession': job.posted_by.profession if job.posted_by.profession else 'Profession Not Specified',
            'posted_by_about': "Work on cutting edge technology >>Do what everyone is doing. Must be a team player >> Must not question authority."
        })
        return posted_by

    def job(self, job_identifier):
        try:
            return Job.objects.get(identifier=job_identifier)
        except Job.DoesNotExist:
            return False
