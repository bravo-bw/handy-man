import factory

from handy_man.main_apps.user_profile.tests.factories import UserProfileFactory
from handy_man.main_apps.job.tests.factories import JobTypeFactory

from handy_man.main_apps.job.models import Job, JobRequest


class JobFactory(factory.DjangoModelFactory):

    class Meta:
        model = Job

    posted_by = factory.SubFactory(UserProfileFactory)
    job_type = factory.SubFactory(JobTypeFactory)
    allocated_to = None
    status = 'new'
jobs = Job.objects.all()
for j in jobs:
    j.job_image_1 = '/Users/tsetsiba/source/handy-man/handy_man/media/default_avatar_male.jpg'
    j.job_image_2 = '/Users/tsetsiba/source/handy-man/handy_man/media/default_avatar_male.jpg'
    j.job_image_3 = '/Users/tsetsiba/source/handy-man/handy_man/media/default_avatar_male.jpg'
    j.save()
