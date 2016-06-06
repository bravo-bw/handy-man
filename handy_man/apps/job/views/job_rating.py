from django.contrib import messages 
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard

from ..models import Quote, Job


class JobRatingView(BaseDashboard):

    template_name = 'user_profile.html'

    def __init__(self):
        super(JobRatingView, self).__init__()

    def get(self, request, *args, **kwargs):
        self.context.update({
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
