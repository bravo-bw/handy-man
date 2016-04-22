from django.conf.urls import url


from .views import JobAllocationView, JobPostingView, JobInterestView

urlpatterns = [
    url(r'^job_posting/', JobPostingView.as_view(), name='job_posting_url'),
    url(r'^job_allocation/', JobAllocationView.as_view(), name='jobs_url'),
    url(r'^available_jobs/', JobInterestView.as_view(), name='available_url')
]
