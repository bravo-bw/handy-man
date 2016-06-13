from operator import itemgetter

from django.conf import settings

from handy_man.apps.job.models import Job, Quote


class UserRanking:

    def qualified_for_profession_marks(self, user, job):
        """Returns the marks for the user's qualifications."""
        qualification_marks = 0
        if user.profession.profession_type == job.job_type.name and user.profession.code == job.job_type.code:
            qualification_marks = settings.QUALIFICATION_WEIGHT
        return qualification_marks

    def job_rate_marks(self, quote_job_rate, standard_job_rate):
        """Returns the marks awarded for pricing."""
        price_marks = (1 / (quote_job_rate - standard_job_rate) / standard_job_rate) * settings.PRICE_WEIGHT
        return price_marks

    def satisfaction_marks(self, user):
        """Return the marks for satisfaction from the customer."""
        thumbs_up = 0
        thumbs_down = 0
        completed_jobs_count = Job.objects.filter(allocated_to=user, status='completed')
        for job in completed_jobs_count:
            thumbs_up += job.rating_likes
            thumbs_down += job.rating_dislikes
        satisfaction_marks = ((thumbs_up - thumbs_down) / settings.MAXIMUM_THUMBS_UP) * settings.SATISFACTION_WEIGHT
        return satisfaction_marks

    def user_jobs_completed_marks(self, user):
        """Returns the marks for the user's jobs that are completed successfully."""
        completed_jobs_count = Job.objects.filter(allocated_to=user, status='completed').count()
        user_jobs_completed_marks = (completed_jobs_count / settings.MAX_COMPLETED_JOBS) * settings.COMPLETED_JOBS_WEIGHT
        return user_jobs_completed_marks

    def user_current_jobs_marks(self, user):
        """Return the marks for the current jobs that are not yet completed."""
        current_jobs = Job.objects.filter(allocated_to=user, status__in=['assigned', 'in_progess']).count()
        user_current_jobs_marks = (1 / (settings.MAX_CURRENT_JOBS - current_jobs) / settings.MAX_CURRENT_JOBS) * settings.IN_PROGRESS_JOBS_WEIGHT
        return user_current_jobs_marks

    def return_ranked_quotations(self, job):
        """Implement to return Y as a ranked list with best being 1st index and worst being last index"""
        ranked_quotes = []
        quotes = Quote.objects.filter(job=job)
        for quote in quotes:
            artisan = quote.artisan
            rank = self.job_rate_marks(quote.rate_per_hour, job.job_type.rate_per_hour) + self.qualified_for_profession_marks(artisan, job) + self.satisfaction_marks(artisan) + self.user_current_jobs_marks(artisan) + self.user_jobs_completed_marks(artisan)
            ranked_quotes.append([quote, rank])
        ranked_quotes.sort(key=itemgetter(1), reverse=True)
        return ranked_quotes
