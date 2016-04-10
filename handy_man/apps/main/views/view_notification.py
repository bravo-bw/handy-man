# import json
# 
# from django.views.generic import View
# from django.shortcuts import render_to_response, redirect
# from django.template import RequestContext, RequestContext
# from .base_dashboard import BaseDashboard
# 
# from ..models import Notification, UserProfile
# from ..constants import NEW, IN_PROGRESS, ACCEPTED, ASSIGNED, COMPLETED
# 
# 
# class ViewNotifications(BaseDashboard):
# 
#     def __init__(self):
#         self.context = {}
#         self.title = 'My Notifications'
#         self.template_name = 'notification.html'
#         super(ViewNotifications, self).__init__()
# 
#     def get(self, request, *args, **kwargs):
#         my_notifications = Notification.objects.filter(owner=UserProfile.objects.get(user=request.user), sent=False)
#         self.context.update({
#             'title': self.title,
#             'my_notifications': my_notifications,
#         })
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
# 
#     def post(self, request, *args, **kwargs):
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))