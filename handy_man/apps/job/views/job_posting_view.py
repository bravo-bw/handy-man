from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard


class JobPostingView(BaseDashboard):

    template_name = 'job_posting.html'

    def __init__(self):
        self.context = {}
        super(JobPostingView, self).__init__()

    def get(self, request, *args, **kwargs):
        self.context.update({
            'name': 'Job Posting View',
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
            'title': self.title
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
