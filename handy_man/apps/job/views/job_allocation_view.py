from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext


class JobAllocationView(View):

    template_name = 'job_allocation.html'

    def __init__(self):
        self.context = {}
        super(JobAllocationView, self).__init__()

    def get(self, request, *args, **kwargs):
        print "def get(self, request, *args, **kwargs):"
        self.context.update({
            'name': 'Setsiba',
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
            'title': self.title
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
