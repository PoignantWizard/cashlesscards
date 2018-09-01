from django.test import TestCase
from djmoney.money import Money

from cashless import customsettings
from cashless.forms import AddCashForm, DeductCashForm


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
