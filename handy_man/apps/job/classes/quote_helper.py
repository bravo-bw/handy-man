class QuoteHelper(object):

    def __init__(self, old_quote):
        self.old_quote = old_quote

    def accept_cancel_qoute(self, accepted):
        self.old_quote.accepted = True if accepted == 'on' else False
        self.old_quote.save()