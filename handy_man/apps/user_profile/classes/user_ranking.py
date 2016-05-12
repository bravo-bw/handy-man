from operator import itemgetter

from ..models import UserProfile
from handy_man.apps.job.models import Job


class UserRanking:

    def qualified_users(self, profession):
        """Return a query-set of qualified users for a certain profession."""
        return UserProfile.objects.filter(profession__profession_type=profession, profession__qualified=True)

    def user_proffesion(self, user):
        """Return the users's profession, for qualified users."""
        profession = "Note qualified."
        if user.profession.qualified:
            profession = user.profession.professoin_type
        return profession

    def qualified_for_profession(self, profession, user):
        """Returns True if a user is qualified for a profession."""
        qualified = False
        if user.profession.profession_type == profession and user.profession.qualified:
            qualified = True
        return qualified

    def user_ranking(self, users, profession):
        """Returns a dictionary of users ranked starting with the highest ranked."""
        ranked_users = []
        for user in users:
            if self.qualified_for_profession(profession, user):
                rank = self.user_rating(user) + self.current_job_points(user) + self.completed_jobs_points(user) + self.qualification_points(user, profession)
                ranked_users.append([user, rank])
        ranked_users.sort(key=itemgetter(1), reverse=True)
        return ranked_users

    def user_rating(self, user):
        """Return the user's average rating."""
        return user.ratings.all()[0].average

    def rated_users(self, users):
        """Returns a list of rated users starting with one with the highest ratings."""
        rated_users = []
        user_ratings = UserProfile.objects.filter(ratings__isnull=False).order_by('ratings__average')
        total_ranked_users = user_ratings.count()
        while total_ranked_users > 0:
            rated_users.append(user_ratings[total_ranked_users - 1])
            total_ranked_users -= 1
        return rated_users

    def user_jobs_completed(self, user):
        """return the number of jobs that have been successfully completed by the user."""
        return Job.objects.filter(allocated_to=user, status='completed').count()

    def user_current_jobs(self, user):
        """Return the number of jobs the user is currently doing."""
        return Job.objects.filter(allocated_to=user, status__in=['assigned', 'in_progess']).count()

    def current_job_points(self, user):
        """Returns point given to a user depending on the jobs they are currently doing."""
        current_jobs_point = 0
        current_jobs_total = self.user_current_jobs(user)
        if current_jobs_total >= 5:
            current_jobs_point = 0
        elif current_jobs_total == 4:
            current_jobs_point = 1
        elif current_jobs_total == 3:
            current_jobs_point = 2
        elif current_jobs_total == 2:
            current_jobs_point = 3
        elif current_jobs_total == 1:
            current_jobs_point = 4
        elif current_jobs_total == 0:
            current_jobs_point = 5
        return current_jobs_point

    def completed_jobs_points(self, user):
        """Returns points for a users based on total number of completed jobs."""
        total_completed_jobs = self.user_jobs_completed(user)
        expirence = 0
        if total_completed_jobs >= 5:
            expirence = 5
        elif total_completed_jobs == 4:
            expirence = 4
        elif total_completed_jobs == 3:
            expirence = 3
        elif total_completed_jobs == 2:
            expirence = 2
        elif total_completed_jobs == 1:
            expirence = 1
        elif total_completed_jobs == 0:
            expirence = 0
        return expirence

    def qualification_points(self, user, profession):
        """Returns points for a user based on their qualification."""
        qualification_points = 0
        if self.qualified_for_proffesion(profession, user):
            qualification_points = 1
        return qualification_points = 0
