"""
Custom settings for cashless app in the cashless cards project
"""

# current version of the system
VERSION = 1.0


# default currency supplied to django-money module
CURRENCY = 'GBP'


# timing options for vouchers
TIMING = (
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("yearly", "Yearly"),
)
