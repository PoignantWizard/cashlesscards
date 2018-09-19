import datetime
from django.test import TestCase
from djmoney.money import Money

from cashless import customsettings
from cashless.models import Voucher, VoucherLink
from cashless.forms import AddCashForm, DeductCashForm, AddVoucherLinkForm, CreateNewVoucherForm


class AddCashFormTest(TestCase):
    """Tests the add cash form"""
    def test_cash_to_add_field_label(self):
        """The field label of the cash to add field is as expected"""
        form = AddCashForm()
        self.assertTrue(form.fields['cash_to_add'].label is None \
        or form.fields['cash_to_add'].label == 'cash to add')

    def test_cash_to_add_field_help_text(self):
        """The help text of the cash to add field is as expected"""
        form = AddCashForm()
        self.assertEqual(form.fields['cash_to_add'].help_text, \
        'Enter a cash value to add to account.')

    def test_cash_to_add_is_zero(self):
        """The form rejects a value of zero"""
        cash = Money(0, customsettings.CURRENCY)
        form = AddCashForm(data={'cash_to_add': cash})
        self.assertFalse(form.is_valid())

    def test_cash_to_add_is_negative(self):
        """The form rejects negative values"""
        cash = Money(-1, customsettings.CURRENCY)
        form = AddCashForm(data={'cash_to_add': cash})
        self.assertFalse(form.is_valid())


class DeductCashFormTest(TestCase):
    """Tests the deduct cash form"""
    def test_cash_to_deduct_field_label(self):
        """The field label of the cash to deduct field is as expected"""
        form = DeductCashForm()
        self.assertTrue(form.fields['cash_to_deduct'].label is None \
        or form.fields['cash_to_deduct'].label == 'cash to deduct')

    def test_cash_to_deduct_field_help_text(self):
        """The help text of the cash to deduct field is as expected"""
        form = DeductCashForm()
        self.assertEqual(form.fields['cash_to_deduct'].help_text, \
        'Enter the cash value of the products to deduct from the account.')

    def test_cash_to_deduct_is_zero(self):
        """The form rejects a value of zero"""
        cash = Money(0, customsettings.CURRENCY)
        form = DeductCashForm(data={'cash_to_deduct': cash})
        self.assertFalse(form.is_valid())

    def test_cash_to_deduct_is_negative(self):
        """The form rejects negative values"""
        cash = Money(-1, customsettings.CURRENCY)
        form = DeductCashForm(data={'cash_to_deduct': cash})
        self.assertFalse(form.is_valid())


class AddVoucherLinkFormTest(TestCase):
    """Tests the add voucher link form"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a voucher
        test_voucher = VoucherLink.objects.create(
            customer_id=1,
            voucher_id=1,
            last_applied=datetime.date.today(),
        )
        test_voucher.save()

    def test_voucher_field_label(self):
        """The field label of the voucher field is as expected"""
        # get test voucher link details
        existing_vouchers = VoucherLink.objects.get(pk=1)
        # test instance
        form = AddVoucherLinkForm(existing_vouchers=existing_vouchers)
        self.assertTrue(form.fields['voucher'].label is None \
        or form.fields['voucher'].label == 'voucher')

    def test_voucher_field_help_text(self):
        """The help text of the voucher field is as expected"""
        # get test voucher link details
        existing_vouchers = VoucherLink.objects.get(pk=1)
        # test instance
        form = AddVoucherLinkForm(existing_vouchers=existing_vouchers)
        self.assertEqual(form.fields['voucher'].help_text, \
        'Select a voucher to assign to this customer.')

    def test_voucher_is_none(self):
        """The form rejects a null value"""
        # get test voucher link details
        existing_vouchers = VoucherLink.objects.get(pk=1)
        # test instance
        no_voucher = None
        form = AddVoucherLinkForm(
            data={
                'voucher': no_voucher
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())

    def test_voucher_already_assigned(self):
        """The form rejects a voucher assignment that already exists"""
        # get test voucher link details
        existing_vouchers = VoucherLink.objects.get(pk=1)
        # test instance
        existing_assignment = 1
        form = AddVoucherLinkForm(
            data={
                'voucher': existing_assignment
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())


class CreateNewVoucherFormTest(TestCase):
    """Tests the create new voucher form"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a voucher
        test_voucher = Voucher.objects.create(
            voucher_application='daily',
            voucher_name='test',
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_voucher.save()

    def test_application_field_lable(self):
        """The field label of the application field is as expected"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        form = CreateNewVoucherForm(existing_vouchers=existing_vouchers)
        self.assertTrue(form.fields['application'].label is None\
        or form.fields['application'].label == 'application')

    def test_name_field_lable(self):
        """The field label of the name field is as expected"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        form = CreateNewVoucherForm(existing_vouchers=existing_vouchers)
        self.assertTrue(form.fields['name'].label is None\
        or form.fields['name'].label == 'name')

    def test_value_field_lable(self):
        """The field label of the value field is as expected"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        form = CreateNewVoucherForm(existing_vouchers=existing_vouchers)
        self.assertTrue(form.fields['value'].label is None\
        or form.fields['value'].label == 'value')

    def test_application_field_help_text(self):
        """The help text of the application field is as expected"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        form = CreateNewVoucherForm(existing_vouchers=existing_vouchers)
        self.assertEqual(form.fields['application'].help_text, \
        "Select how often the voucher is applied to the customer's account.")

    def test_name_field_help_text(self):
        """The help text of the name field is as expected"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        form = CreateNewVoucherForm(existing_vouchers=existing_vouchers)
        self.assertEqual(form.fields['name'].help_text, \
        "Give the voucher a unique name.")

    def test_value_field_help_text(self):
        """The help text of the value field is as expected"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        form = CreateNewVoucherForm(existing_vouchers=existing_vouchers)
        self.assertEqual(form.fields['value'].help_text, \
        'Select the cash value for the voucher.')

    def test_application_is_none(self):
        """The form rejects a null value in the application field"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        test_application = None
        test_name = 'test'
        test_value = Money(1, customsettings.CURRENCY)
        form = CreateNewVoucherForm(
            data={
                'application': test_application,
                'name': test_name,
                'value': test_value,
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())

    def test_name_is_none(self):
        """The form rejects a null value in the name field"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        test_application = 'daily'
        test_name = None
        test_value = Money(1, customsettings.CURRENCY)
        form = CreateNewVoucherForm(
            data={
                'application': test_application,
                'name': test_name,
                'value': test_value,
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())

    def test_name_exists(self):
        """The form rejects a name that already exists"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        test_application = 'daily'
        test_name = 'test'
        test_value = Money(1, customsettings.CURRENCY)
        form = CreateNewVoucherForm(
            data={
                'application': test_application,
                'name': test_name,
                'value': test_value,
            },
            existing_vouchers=existing_vouchers
        )
        form = CreateNewVoucherForm(
            data={
                'application': test_application,
                'name': test_name,
                'value': test_value,
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())

    def test_value_is_zero(self):
        """The form rejects a value of zero"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        test_application = 'daily'
        test_name = 'test'
        test_value = Money(0, customsettings.CURRENCY)
        form = CreateNewVoucherForm(
            data={
                'application': test_application,
                'name': test_name,
                'value': test_value,
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())

    def test_cash_to_deduct_is_negative(self):
        """The form rejects negative values"""
        # get test voucher details
        existing_vouchers = Voucher.objects.get(pk=1)
        # test instance
        test_application = 'daily'
        test_name = 'test'
        test_value = Money(-1, customsettings.CURRENCY)
        form = CreateNewVoucherForm(
            data={
                'application': test_application,
                'name': test_name,
                'value': test_value,
            },
            existing_vouchers=existing_vouchers
        )
        self.assertFalse(form.is_valid())
