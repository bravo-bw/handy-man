from django.contrib import messages 
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard


class JobAllocationView(BaseDashboard):

    template_name = 'job_allocation.html'

    def __init__(self):
        self.context = {}
        super(JobAllocationView, self).__init__()

    def get(self, request, *args, **kwargs):
        self.context.update({
            'name': 'Setsiba',
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        print("job_id:", request.POST.get('job_id'))
        messages.success(request, "Successfully assigned to setsiba Tshepiso.")
#         job_allocation_form = JobAllocationForm(request.POST or None)
#         if job_allocation_form.is_valid():
#             instance = job_allocation_form.save(commit=False)
#             instance.save()
#             messages.success(request, "Successfully assigned to setsiba Tshepiso.")
#         else:
#            messages.success(request, "Successfully assigned to setsiba Tshepiso.") 
        self.context.update({
            'title': self.title,
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
