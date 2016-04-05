import json

from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from .base_dashboard import BaseDashboard
from ..models import UserProfile


class AccountDetails(BaseDashboard):

    def __init__(self):
        self.context = {}
        self.template_name = 'account_details.html'
        super(AccountDetails, self).__init__()

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        self.context.update({
            'user_profile': user_profile,
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
