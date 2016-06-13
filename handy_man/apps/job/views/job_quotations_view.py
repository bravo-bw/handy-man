from django.contrib import messages 
from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.apps.main.views.base_dashboard import BaseDashboard
from handy_man.apps.user_profile.models.profile import UserProfile
from handy_man.apps.user_profile.classes import MenuConfiguration, UserRanking

from ..models import Quote, Job
from ..classes import QuoteHelper, JobHelper
from ..forms import QuotationForm


class JobQuotationsView(BaseDashboard):

    template_name = 'job_quotations.html'

    def __init__(self):
        super(JobQuotationsView, self).__init__()

    def get(self, request, *args, **kwargs):
        loggedin_user_profile = UserProfile.objects.get(user=request.user)
        if request.GET.get('hidden_job_id'):
            form = QuotationForm(request.GET)
            self.template_name = 'submit_quotation.html'
            self.context.update({
                #'ranked_quotes': UserRanking().return_ranked_quotations(form.cleaned_data.get('job')),
                'form': form,
                'loggedin_user_profile': loggedin_user_profile,
                'job': Job.objects.get(pk=request.GET.get('hidden_job_id')),
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        else:
            job = Job.objects.get(pk=kwargs.get('job'))
            self.context.update({
                'can_add_quote': JobHelper(job=job).allow_add_quote(loggedin_user_profile),
                'ranked_quotes': UserRanking().return_ranked_quotations(job),
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
            if request.POST.get('quote_id'):
                # Update, can only update accepted field.
                quote = Quote.objects.get(pk=int(request.POST.get('quote_id')[0]))
                quote_helper = QuoteHelper(quote)
                new_quote = quote_helper.accept_cancel_qoute(request.POST.get('accepted'))
                new_quote.save()
            else:
                form.save()
            self.context.update({
                'can_add_quote': JobHelper(job=form.cleaned_data.get('job')).allow_add_quote(loggedin_user_profile),
                'ranked_quotes': UserRanking().return_ranked_quotations(form.cleaned_data.get('job')),
#                 'ranked_quotes': Quote.objects.filter(job=form.cleaned_data.get('job')), # For testing purposes
                'loggedin_user_profile': loggedin_user_profile,
                'job': form.cleaned_data.get('job'),
                'quotes': Quote.objects.filter(job=form.cleaned_data.get('job')),
                'menus': MenuConfiguration().user_menu_list(loggedin_user_profile)
            })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
