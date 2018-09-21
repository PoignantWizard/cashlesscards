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


class CreateNewVoucherForm(forms.Form):
    """Generates the form for creating a new voucher"""

    def __init__(self, *args, **kwargs):
        """Initializes the form to handle special arguments"""
        self.existing_vouchers = kwargs.pop('existing_vouchers')
        super(CreateNewVoucherForm, self).__init__(*args, **kwargs)

    application = forms.ChoiceField(
        choices=customsettings.TIMING,
        help_text="Select how often the voucher is applied to the customer's account."
    )
    name = forms.CharField(
        max_length=255,
        help_text="Give the voucher a unique name."
    )
    value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        help_text="Select the cash value for the voucher."
    )

    def clean_voucher_application(self):
        """cleans up user data before creating voucher"""
        v_application = self.cleaned_data['application']

        # Check that a voucher application period has been selected
        if not v_application:
            raise ValidationError(ugettext_lazy('Invalid value - no application period selected'))

        # Return the cleaned data
        return v_application

    def clean_voucher_name(self):
        """cleans up user data before creating voucher"""
        v_name = self.cleaned_data['name']

        # Check that a voucher name has been selected
        if not v_name:
            raise ValidationError(ugettext_lazy('Invalid value - no voucher name entered'))

        # Check if a voucher already exists
        if v_name in self.existing_vouchers:
            raise ValidationError(ugettext_lazy(
                'Invalid value - voucher already exists'
            ))

        # Return the cleaned data
        return v_name

    def clean_voucher_value(self):
        """cleans up user data before creating voucher"""
        v_value = self.cleaned_data['value']

        # Check value is not negative
        if v_value < Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - cash value is negative'))

        # Check value is not zero
        if v_value == Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - cash value is zero'))

        # Return the cleaned data
        return v_value


class CreateNewCustomerForm(forms.Form):
    """Generates the form for creating a new customer account"""

    def __init__(self, *args, **kwargs):
        """Initializes the form to handle special arguments"""
        self.existing_cards = kwargs.pop('existing_cards')
        super(CreateNewCustomerForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(
        max_length=255,
        help_text="Enter the customer's first name."
    )
    surname = forms.CharField(
        max_length=255,
        help_text="Enter the customer's last name."
    )
    card_number = forms.IntegerField(
        help_text="Enter the customer's card number to associate a cash account."
    )
    opening_balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        help_text="Select the opening balance for the cash account."
    )

    def clean_customer_first_name(self):
        """cleans up user data before creating customer account"""
        c_first_name = self.cleaned_data['first_name']

        # Check that a customer name has been selected
        if not c_first_name:
            raise ValidationError(ugettext_lazy('Invalid value - no customer first name entered'))

        # Return the cleaned data
        return c_first_name

    def clean_customer_surname(self):
        """cleans up user data before creating customer account"""
        c_surname = self.cleaned_data['surname']

        # Check that a customer name has been selected
        if not c_surname:
            raise ValidationError(ugettext_lazy('Invalid value - no customer last name entered'))

        # Return the cleaned data
        return c_surname

    def clean_card_number(self):
        """cleans up user data before creating customer account"""
        c_card_number = self.cleaned_data['card_number']

        # Check that a card number has been selected
        if not c_card_number:
            raise ValidationError(ugettext_lazy('Invalid value - no card number entered'))

        # Check that card number is not zero
        if c_card_number == 0:
            raise ValidationError(ugettext_lazy("Invalid value - card number can't be zero"))

        # Check that card number is not negative
        if c_card_number < 0:
            raise ValidationError(ugettext_lazy("Invalid value - card number can't be negative"))

        # Check if a card number already exists
        if c_card_number in self.existing_cards:
            raise ValidationError(ugettext_lazy(
                'Invalid value - a card with this number already exists on the system'
            ))

        # Return the cleaned data
        return c_card_number

    def clean_opening_balance(self):
        """cleans up user data before creating customer account"""
        c_opening_balance = self.cleaned_data['opening_balance']

        # Check value is not negative
        if c_opening_balance < Money(0, customsettings.CURRENCY):
            raise ValidationError(ugettext_lazy('Invalid value - opening balance is negative'))

        # Return the cleaned data
        return c_opening_balance
