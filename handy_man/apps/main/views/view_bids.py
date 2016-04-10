# import json
# 
# from django.views.generic import View
# from django.shortcuts import render_to_response, redirect
# from django.template import RequestContext, RequestContext
# from .base_dashboard import BaseDashboard
# 
# from ..models import Job, Bid
# from ..constants import NEW, IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED
# 
# 
# class ViewBids(BaseDashboard):
# 
#     def __init__(self):
#         self.context = {}
#         self.template_name = 'shipper.html'
#         super(ViewBids, self).__init__()
# 
#     def get(self, request, *args, **kwargs):
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
# 
#     def post(self, request, *args, **kwargs):
#         job = Job.objects.get(job_identifier=request.POST.get('job_identifier'))
#         public_jobs = [job, ]
#         my_jobs = Job.objects.filter(job_status__in=[IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED],
#                                      exercutor__user__username=request.user.username)
#         job_bids = Bid.objects.filter(job=job)
#         if request.POST.get('job_type') == 'available_jobs':
#             self.template_name = "shipper_available_jobs.html"
#         else:
#             self.template_name = "shipper.html"
#         self.context.update({
#             'title': self.title,
#             'public_jobs': public_jobs,
#             'my_jobs': my_jobs,
#             'job_bids': job_bids
#         })
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))