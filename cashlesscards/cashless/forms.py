from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from djmoney.forms.fields import MoneyField
from djmoney.money import Money

from . import customsettings


class AddCashForm(forms.Form):
    """Generates the form for adding cash to a customer's account"""
    cash_to_add = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        help_text="Enter a cash value to add to account."
    )

    def clean_cash_to_add(self):
        """cleans up user data before adding cash"""
        data = self.cleaned_data['cash_to_add']

        # Check value is not negative
        if data < Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - cash value is negative'))

        # Check value is not zero
        if data == Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - cash value is zero'))

        # Return the cleaned data
        return data


class DeductCashForm(forms.Form):
    """Generates the form for subtracting cash
    from a customer's account after purchasing something"""
    cash_to_deduct = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        help_text="Enter the cash value of the products to deduct from the account."
    )

    def clean_cash_to_deduct(self):
        """cleans up user data before deducting cash"""
        data = self.cleaned_data['cash_to_deduct']

        # Check value is not negative
        if data < Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - cash value is negative'))

        # Check value is not zero
        if data == Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - cash value is zero'))

        # Return the cleaned data
        return data
