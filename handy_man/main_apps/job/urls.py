from django.conf.urls import url

from .views import (
    JobAllocationView, JobPostingView, JobInterestView, JobQuotationsView, JobTimelineView, JobDisplayView, ModifyJob)


urlpatterns = [
    url(r'^job_posting/', JobPostingView.as_view(), name='job_posting_url'),
    url(r'^job_allocation/', JobAllocationView.as_view(), name='jobs_url'),
    url(r'^job_quote/(?P<job>.*)/$', JobQuotationsView.as_view(), name='quote_url'),
    url(r'^available_jobs/', JobInterestView.as_view(), name='available_url'),
    url(r'^job_timeline/(?P<job_identifier>.*)/', JobTimelineView.as_view(), name='job_timeline_url'),
    url(r'^modify_job/(?P<job_identifier>.*)/', ModifyJob.as_view(), name='modify_job_url'),
    url(r'^job_display/(?P<job_identifier>.*)/', JobDisplayView.as_view(), name='job_display_url'),

]