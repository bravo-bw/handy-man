from django.db import models


class Job(models.Model):

    """
    This model describes the job and its details.
         1. Job Posting
         2. Job Allocation
         3. Job Quatation
         4. Job Payment
         5. Job Report
    """

    #user = models.ForeignKey(UserProfile, related_name='profile_sumbittor', editable=False)

    #exercutor = models.ForeignKey(UserProfile, null=True, editable=False)

    identifier = models.CharField(
        verbose_name='Job Identifier',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    category = models.CharField(
        verbose_name='Category',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    job_images = models.CharField(
        verbose_name='Images',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    location = models.CharField(
        verbose_name='Location',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

#     area = models.CharField(
#         verbose_name='Area',
#         default=None,
#         max_length=36,
#         unique=True,
#         editable=False
#     )

    status = models.CharField(
        verbose_name='Job Status',
        max_length=10,
        default=NEW,
        choices=JOB_STATUS,
        editable=False
    )

    type = models.CharField(
        verbose_name='Job Type',
        max_length=25,
        choices=JOB_TYPE,
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name='Detailed description of Job',
        max_length=250,
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'job'
