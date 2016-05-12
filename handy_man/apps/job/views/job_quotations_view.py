from django.contrib import messages 
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.user_profile.models.profile import UserProfile
from handy_man.apps.user_profile.classes import MenuConfiguration

from ..models import Quote, Job
from ..forms import QuotationForm


class JobQuotationsView(BaseDashboard):

    template_name = 'job_quotations.html'

    def __init__(self):
        super(JobQuotationsView, self).__init__()

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        if request.GET.get('hidden_job_id'):
            self.template_name = 'submit_quotation.html'
            self.context.update({
                'loggedin_user_profile': loggedin_user_profile,
                'job': Job.objects.get(pk=request.GET.get('hidden_job_id')),
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        else:
            job = Job.objects.get(pk=kwargs.get('job_id'))
            self.context.update({
                'loggedin_user_profile': loggedin_user_profile,
                'job': job,
                'quotes': Quote.objects.filter(job=job),
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        form = QuotationForm(request.POST)
        if form.is_valid():
            job = Job.objects.get(pk=kwargs.get('job_id'))
            if request.POST.get('quote_id'):
                # Update, can only update accepted field.
                quote = Quote.objects.get(pk=int(request.POST.get('quote_id')[0]))
                print(request.POST.get('accepted'))
                quote.accepted = True if request.POST.get('accepted') == 'on' else False
            else:
                # new instance.
                quote = form.instance
            quote.job = job
            quote.save()
            self.context.update({
                'loggedin_user_profile': loggedin_user_profile,
                'job': job,
                'quotes': Quote.objects.filter(job=job),
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
