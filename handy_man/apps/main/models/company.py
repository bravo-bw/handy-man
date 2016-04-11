# from django.db import models
# 
# 
# class Company(models.Model):
# 
#     '''
#     This model gives a description of the company details.
#     '''
# 
#     name = models.CharField(
#         verbose_name='Company name',
#         max_length=25,
#         unique=True,
#         null=True,
#         blank=True,)
# 
#     tax_id_number = models.CharField(
#         verbose_name='Tax number',
#         max_length=25,
#         null=True,
#         blank=True,
#     )
# 
#     class Meta:
#         app_label = 'main'
