# import json
# 
# from django.views.generic import View
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.http.response import HttpResponse
# 
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from .base_dashboard import BaseDashboard
# 
# from ..models import Job
# from ..constants import NEW, IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED
# from handy_man.apps.main.models.bid import Bid
# 
# 
# class Shipper(BaseDashboard):
# 
#     def __init__(self):
#         self.context = {}
#         self.template_name = 'shipper.html'
#         super(Shipper, self).__init__()
# 
#     def get(self, request, *args, **kwargs):
#         notifications = 'Notifications.objects.all()'
#         job_identifier = request.GET.get("job_identifier")
#         change_job = request.GET.get("change_job")
#         if job_identifier:
#             public_jobs = Job.objects.filter(job_status__in=[NEW], job_identifier=job_identifier)
#         else:
#             public_jobs = Job.objects.filter(job_status__in=[NEW])
# 
#         if change_job:
#             change_job = request.GET.get("change_job")
#             new_status = None
#             for vl in range(100):
#                 name = "job_status" + str(vl)
#                 if request.GET.get(name):
#                     new_status = request.GET.get(name)
#                     break
#             try:
#                 job = Job.objects.get(job_identifier=request.GET.get('job_identifier'))
#                 job.job_status = new_status
#                 job.save()
#             except Job.DoesNotExist:
#                 pass
#         public_jobs = Job.objects.filter(job_status__in=[NEW])
#         my_jobs = Job.objects.filter(job_status__in=[IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED],
#                                      exercutor__user__username=request.user.username)
#         if request.GET.get('job_type') == 'available_jobs':
#             self.template_name = "shipper_available_jobs.html"
#         else:
#             self.template_name = "shipper.html"
# 
#         truck_plan_coordinates = [
#             [-24.619168, 25.934612],
#             [-24.378842, 26.062498],
#             [-24.348581, 26.086359],
#             [-24.025998, 26.317072],
#             [-23.146262, 26.819975],
#             [-21.949307, 27.301839],
#             [-21.179817, 27.510579]
#         ]
#         destination = [-21.179817, 27.510579]
#         self.context.update({
#             'title': self.title,
#             'notifications': notifications,
#             'public_jobs': public_jobs,
#             'my_jobs': my_jobs,
#             'truck_plan_coordinates': truck_plan_coordinates,
#             'coordinates_list_len': len(truck_plan_coordinates),
#             'destination': destination,
#         })
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
# 
#     def post(self, request, *args, **kwargs):
#         self.context.update({
#             'title': self.title
#         })
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
# 
#     def get_context_data(self, **kwargs):
#         return super(Shipper, self).get_context_data(**kwargs)
# 
#     def job_biddings(self, job_identifier=None):
#         return Bid.objects.filter(job__job_identifier=job_identifier)
# 
# 
# def create_get(request):
#     if request.method == 'GET':
#         post_text = request.GET.get('job_type')
#         response_data = dict({"job_type": "My Job"})
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#     else:
#         response_data = dict({"job_type": "My Job"})
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )

