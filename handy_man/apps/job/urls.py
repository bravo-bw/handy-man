from django.conf.urls import url


from .views.job_allocation_view import JobAllocationView

urlpatterns = [
    url(r'^$', JobAllocationView.as_view(), name='jobs_url'),
]
