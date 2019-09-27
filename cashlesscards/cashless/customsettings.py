"""
Custom settings for cashless app in the cashless cards project
"""

# current version of the system
VERSION = 1.0


# language and timezone settings
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GB'


# default currency supplied to django-money module
CURRENCY = 'GBP'


# email for sending password reset tokens
FROM_EMAIL = 'cashlesscards@localhost'


# timing options for vouchers
# delete rows to remove options from system
# currently doesn't support custom timings
TIMING = (
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("yearly", "Yearly"),
)

# enable stripe.js integration\n" \
USE_STRIPE = True

# minimum value accepted by stripe.js card payment
# see https://stripe.com/docs/currencies#minimum-and-maximum-charge-amounts
# for details of absolute stripe.js minimums
MINIMUM_CARD_PAYMENT_VALUE = 0.3
