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
