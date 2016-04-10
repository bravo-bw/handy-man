# from django.db import models
# 
# from ..constants import NEW, UNDER_CONSIDERATION, REJECTED
# from .job import Job
# from handy_man.apps.user_profile.models.profile import UserProfile
# 
# 
# class Bid(models.Model):
# 
#     '''
#     This model describes the bids that companies are making against a job.
#     '''
# 
#     job = models.ForeignKey(Job)
# 
#     bid_owner = models.ForeignKey(UserProfile)
# 
#     bid_status = models.CharField(
#         verbose_name='Bid Status',
#         max_length=20,
#         default=NEW,
#     )
# 
#     bidding_amount = models.DecimalField(
#         verbose_name='Amount in Pula',
#         max_digits=10,
#         decimal_places=2
#     )
# 
#     expired = models.BooleanField(default=False)
# 
#     def email_notification_options(self):
#         message_to = self.bid_owner.user.email
#         subject = "Bid for job '{}' has been modified".format(self.job.job_identifier)
#         message = "status={}, amount={}".format(self.bid_status, self.bidding_amount)
#         owner = self.bid_owner
#         return (message_to, subject, message, owner)
# 
#     class Meta:
#         app_label = 'main'
