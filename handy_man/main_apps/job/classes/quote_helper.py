from django.apps import apps
from django.core.exceptions import ValidationError

from handy_man.main_apps.main.constants import NEW


class QuoteHelper(object):

    def __init__(self, quote):
        self.quote = quote

    def accept_cancel_qoute(self, accepted, allocated_to):
        # This method is only called from the view. 'accepted' can only be set to False by the helper when quote
        # is getting rejected.
        self.quote.accepted = True if accepted == 'on' else None
        if self.quote.accepted:
            self.quote.job.allocated_to = allocated_to
        else:
            self.quote.job.allocated_to = None
        self.quote.job.save()
        return self.quote

    def reject_all_other_quotes(self):
        Quote = apps.get_model('job', 'Quote')
        Quote.objects.filter(job=self.quote.job).exclude(pk=self.quote.pk).update(accepted=False)

    def open_rejected_quotes(self):
        Quote = apps.get_model('job', 'Quote')
        Quote.objects.filter(job=self.quote.job, accepted=False).update(accepted=None)

    def requote_job(self):
        Quote = apps.get_model('job', 'Quote')
        if not Quote.objects.filter(job=self.quote.job, artisan=self.quote.artisan).exists():
            pass
        else:
            # This is an attempt to re-quote, close all open quotes. Recall that this Quote is not persisted yet.
            Quote.objects.filter(job=self.quote.job, artisan=self.quote.artisan, closed_requoted=False).update(
                closed_requoted=True)

    def process(self):
        # Attempting to create a new Quote
        if not self.quote.pk:
            # Ensure its being created by right user of correct Profession
            if not self.quote.artisan.profession:
                raise ValidationError('Only Artisans allowed to create quotations.')
            elif self.quote.artisan.profession.code != self.quote.job.job_type.code:
                raise ValidationError('Attempting to create a quotation for an incompatible profession.')
            # Check for correct job status
            elif self.quote.job.status != NEW:
                raise ValidationError(
                    'Can only create quotation on a job of status NEW. current status is {}'.format(
                        self.quote.job.status))
            # Now we deal with the artisan's perspective, that includes:
            # Trying to re-quote for a job.
            self.requote_job()
        # Now we are attempting to update existing quotation.
        else:
            # First we deal with the customer's perspective, that includes:
            # Accepting Quote
            # Un-Accepting Quote
            if self.quote.accepted:
                # If we are accepting this quote then reject all other quotes for this job (exclude myself)
                self.reject_all_other_quotes()
            # Note, we explicitly want to test for False, we don't want to catch None
            elif self.quote.accepted is None:
                self.open_rejected_quotes()
            else:
                pass