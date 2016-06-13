from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from handy_man.apps.job.models.job import Job


class JobDisplayView(TemplateView):

    template_name = 'display_job.html'

    def __init__(self):
        super(JobDisplayView, self).__init__()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JobDisplayView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobDisplayView, self).get_context_data(**kwargs)
        context.update(
            job_identifier=self.kwargs.get('job_identifier'),
        )
        return context

    def job_image_name(self, job_image):
        if self.job:
            return job_image.split('/')[-1]
        return ''

    def job_images(self):
        job = self.job
        if job:
            return [self.job_image_name(job.job_image_1), self.job_image_name(job.job_image_2), self.job_image_name(job.job_image_3)]
        return []

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        job_identifier = context.get('job_identifier')
        job_identifier = int(job_identifier.split('/')[0])
        job = self.job(job_identifier)
        context.update({
            'job': job,
            #'job_images': self.job_images()
        })
        return render(request, self.template_name, context)

    def job(self, job_identifier):
        try:
            return Job.objects.get(identifier=job_identifier)
        except Job.DoesNotExist:
            return False
