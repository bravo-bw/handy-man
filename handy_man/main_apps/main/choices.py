SENDING_METHODS = (
    ('sms', 'SMS'),
    ('email', 'email'),
)

ACCOUNT_TYPE = (('artisan', 'Artisan'),
                ('sme', 'SME'),
                ('customer', 'Customer'))

JOB_STATUS = (('new', 'New'),
              ('in_progess', 'In Progress'),
              ('assigned', 'Assign'),
              ('completed', 'Completed'))

PAYMENT_MODE = (
    ('bank_deposit', 'Bank Deposit'),
    ('eft', 'Electronic Funds Transfer'),
    ('cash', 'Cash'),
    ('card', 'Card'),
)

PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('complete', 'Complete'),
    ('declined', 'Declined'),
    ('reversed', 'Reversed'),
    ('confirmed', 'Confirmed'),
)

BID_STATUS = (
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('submited', 'Submitted'),
    ('under_consideration', 'Under Consideration')
)

BANK = (
    ('fnb', 'First National Bank'),
    ('bank_gaborone', 'Bank Gaborone'),
    ('stanbic', 'Stanbic Bank'),
    ('bank_abc', 'BancAbc'),
    ('bank_india', 'Bank Of India'),
    ('bank_baroda', 'Bank of Baroda'),
    ('standard_bank', 'Standard Bank'),
    ('baclays_bank', 'Baclays Bank'),
    ('western_union', 'Western Union'),
    ('pay_pal', 'Pay Pal'),
)

CARGO_TYPE = (
    ('harzard', 'Harzardous Material'),
    ('preshable', 'Perishables'),
    ('fragile', 'Fragile'),
    ('mechanical', 'Mechanical'),
)

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

BANK_ACCOUNT_TYPE = (
    ('savings', 'Savings'),
    ('current', 'Current'),
    ('business', 'Business'),
    ('loan', 'Loan'),
)

JOB_TYPE = (
    ('carpentry', 'Carpentry'),
    ('plumbing', 'Plumbing'),
    ('brick_laying', 'Brick Laying'),
    ('tile_laying', 'Tile Laying'))

ARTISAN_PROFESSION = (
    ('carpenter', 'Carpenter'),
    ('plumber', 'Plumber'),
    ('electrician', 'Electrician'),
    ('brick_layer', 'Brick Layer'),
    ('tiler', 'Tiler'),
    ('roofer', 'Roofer'),
    ('gardener', 'Gardener'),
    ('mechanic', 'Mechanic'),
    ('auto_electrician', 'Auto Electrician'),
    ('panel_beater', 'Panel Beater'),
)

CURRENCY = (('BWP', 'pula'),
            ('ZAR', 's.a rands'),
            ('USD', 'u.s dollar'))
