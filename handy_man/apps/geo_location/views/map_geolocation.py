from django.shortcuts import render_to_response
from django.template import RequestContext
from handy_man.apps.main.views import BaseDashboard


class MapGeolocation(BaseDashboard):

    def __init__(self):
        self.context = {}
        self.template_name = 'map_include.html'

    def get(self, request, *args, **kwargs):
        self.context.update({
            'latitude': -24.3453,
            'longitude': 24.45354,
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):

        return super(MapGeolocation, self).get_context_data(**kwargs)
