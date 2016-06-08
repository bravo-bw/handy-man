from django.conf.urls import url

from .views import JobAllocationView, JobPostingView, JobInterestView, JobQuotationsView, JobTimelineView


urlpatterns = [
    url(r'^job_posting/', JobPostingView.as_view(), name='job_posting_url'),
    url(r'^job_allocation/', JobAllocationView.as_view(), name='jobs_url'),
    url(r'^job_quote/(?P<job>[0-9]{1,4})/$', JobQuotationsView.as_view(), name='quote_url'),
    url(r'^available_jobs/', JobInterestView.as_view(), name='available_url'),
    url(r'^job_timeline/(?P<job_identifier>.*)/', JobTimelineView.as_view(), name='job_timeline_url'),

]
