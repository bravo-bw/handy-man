from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext


class BaseDashboard(View):

    def __init__(self):
        self.context = {}
        self.title = 'BW Handy Man'
        self.coordinates = [-22.323764, 23.793962]

    def get(self, request, *args, **kwargs):
        self.context.update({
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):
        return super(BaseDashboard, self).get_context_data(**kwargs)
