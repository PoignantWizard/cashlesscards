from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from djmoney.forms.fields import MoneyField
from djmoney.money import Money

from . import customsettings
from .models import Voucher


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


class AddVoucherLinkForm(forms.Form):
    """Generates the form for adding a voucher to a customer's record"""

    def __init__(self, *args, **kwargs):
        """Initializes the form to handle special arguments"""
        self.existing_vouchers = kwargs.pop('existing_vouchers')
        super(AddVoucherLinkForm, self).__init__(*args, **kwargs)

    voucher = forms.ModelChoiceField(
        queryset=Voucher.objects.all().order_by('voucher_name'),
        to_field_name="pk",
        help_text="Select a voucher to assign to this customer."
    )

    def clean_voucher(self):
        """cleans up user data before assigning voucher"""
        data = self.cleaned_data['voucher']

        # Check that a voucher has been selected
        if not data:
            raise ValidationError(ugettext_lazy('Invalid value - no voucher selected'))

        # Extract the voucher primary key
        data = data.pk

        # Check if a voucher is already assigned
        if data in self.existing_vouchers:
            raise ValidationError(ugettext_lazy(
                'Invalid value - voucher already assigned to customer'
            ))

        # Return the cleaned data
        return data
