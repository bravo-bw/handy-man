from django.db import models


class Job(models.Model):

    """
    This model describes the job and its details.
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
        verbose_name='Category',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    region = models.CharField(
        verbose_name='Category',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    area = models.CharField(
        verbose_name='Category',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    status = models.CharField(
        verbose_name='Job Status',
        max_length=10,
        default=NEW,
        choices=JOB_STATUS,
        editable=False
    )

    type = models.CharField(
        verbose_name='Type of Cargo',
        max_length=25,
        choices=CARGO_TYPE,
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name='Detailed description of Cargo',
        max_length=250,
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'job'
