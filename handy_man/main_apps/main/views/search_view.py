from django.shortcuts import render_to_response
from django.template import RequestContext

from handy_man.main_apps.main.views import BaseDashboard
from handy_man.main_apps.user_profile.models import UserProfile


class SearchView(BaseDashboard):
    def __init__(self):
        self.context = {}
        self.template_name = 'search.html'
        super(SearchView, self).__init__()

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            search_value = request.POST.get('search_val')
            model = request.POST.get('select1')
            if model == 'profiles':
                SearchModel = UserProfile
            elif model == 'jobs':
                pass
            else:
                pass
            # TODO: Use Q objects here and do an OR
            results = SearchModel.objects.filter(user__username__icontains=search_value)
            self.context.update({
                'title': self.title,
                'user_profiles': results,
            })
        else:
            pass
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):
        return super(SearchView, self).get_context_data(**kwargs)
