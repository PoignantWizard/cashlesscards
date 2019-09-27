import datetime
from django.test import TestCase
from djmoney.money import Money

from cashless import customsettings
from cashless.models import Voucher, VoucherLink, Customer
from cashless.forms import AddCashForm, DeductCashForm, AddVoucherLinkForm
from cashless.forms import CreateNewVoucherForm, CreateNewCustomerForm


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


class AddCashForStripePaymentFormTest(TestCase):
    """Tests the add cash for stripe.js payment form"""
    def test_cash_to_add_field_label(self):
        """The field label of the cash to add field is as expected"""
        form = AddCashForStripePaymentFormTest()
        self.assertTrue(form.fields['cash_to_add'].label is None \
        or form.fields['cash_to_add'].label == 'cash to add')

    def test_cash_to_add_field_help_text(self):
        """The help text of the cash to add field is as expected"""
        form = AddCashForm()
        self.assertEqual(form.fields['cash_to_add'].help_text, \
        'Enter a value to add to account.')

    def test_cash_to_add_is_zero(self):
        """The form rejects a value of zero"""
        cash = Money(0, customsettings.CURRENCY)
        form = AddCashForm(data={'cash_to_add': cash})
        self.assertFalse(form.is_valid())

    def test_cash_to_add_is_below_minimum(self):
        """The form rejects values below the minimum"""
        cash = Money(customsettings.MINIMUM_CARD_PAYMENT_VALUE, customsettings.CURRENCY)
        form = AddCashForm(data={'cash_to_add': cash})
        self.assertFalse(form.is_valid())

    def test_cash_to_add_is_above_maximum(self):
        """The form rejects values below the minimum"""
        cash = Money(999999.99, customsettings.CURRENCY)
        form = AddCashForm(data={'cash_to_add': cash})
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


class CreateNewCustomerFormTest(TestCase):
    """Tests the create new customer account form"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create test customers
        test_customer1 = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )
        test_customer2 = Customer.objects.create(
            card_number=98,
            first_name='Sophie',
            surname='Smith',
        )
        test_customer1.save()
        test_customer2.save()

    def test_card_number_field_lable(self):
        """The field label of the card number field is as expected"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        form = CreateNewCustomerForm(existing_cards=existing_cards)
        self.assertTrue(form.fields['card_number'].label is None\
        or form.fields['card_number'].label == 'card number')

    def test_first_name_field_lable(self):
        """The field label of the first name field is as expected"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        form = CreateNewCustomerForm(existing_cards=existing_cards)
        self.assertTrue(form.fields['first_name'].label is None\
        or form.fields['first_name'].label == 'first name')

    def test_surname_field_lable(self):
        """The field label of the surname field is as expected"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        form = CreateNewCustomerForm(existing_cards=existing_cards)
        self.assertTrue(form.fields['surname'].label is None\
        or form.fields['surname'].label == 'surname')

    def test_opening_balance_field_lable(self):
        """The field label of the opening balance field is as expected"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        form = CreateNewCustomerForm(existing_cards=existing_cards)
        self.assertTrue(form.fields['opening_balance'].label is None\
        or form.fields['opening_balance'].label == 'opening balance')

    def test_first_name_is_none(self):
        """The form rejects a null value in the first name field"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        test_first_name = None
        test_surname = 'test'
        test_card_number = 1
        test_opening_balance = Money(1, customsettings.CURRENCY)
        form = CreateNewCustomerForm(
            data={
                'first_name': test_first_name,
                'surname': test_surname,
                'card_number': test_card_number,
                'opening_balance': test_opening_balance,
            },
            existing_cards=existing_cards
        )
        self.assertFalse(form.is_valid())

    def test_surname_is_none(self):
        """The form rejects a null value in the surname field"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        test_first_name = 'test'
        test_surname = None
        test_card_number = 1
        test_opening_balance = Money(1, customsettings.CURRENCY)
        form = CreateNewCustomerForm(
            data={
                'first_name': test_first_name,
                'surname': test_surname,
                'card_number': test_card_number,
                'opening_balance': test_opening_balance,
            },
            existing_cards=existing_cards
        )
        self.assertFalse(form.is_valid())

    def test_card_number_exists(self):
        """The form rejects a card number that already exists"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        test_first_name = 'test'
        test_surname = 'test'
        test_card_number = 1
        test_opening_balance = Money(1, customsettings.CURRENCY)
        form = CreateNewCustomerForm(
            data={
                'first_name': test_first_name,
                'surname': test_surname,
                'card_number': test_card_number,
                'opening_balance': test_opening_balance,
            },
            existing_cards=existing_cards
        )
        form = CreateNewCustomerForm(
            data={
                'first_name': test_first_name,
                'surname': test_surname,
                'card_number': test_card_number,
                'opening_balance': test_opening_balance,
            },
            existing_cards=existing_cards
        )
        self.assertFalse(form.is_valid())

    def test_card_number_is_zero(self):
        """The form rejects a card number of zero"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        test_first_name = 'test'
        test_surname = 'test'
        test_card_number = 0
        test_opening_balance = Money(1, customsettings.CURRENCY)
        form = CreateNewCustomerForm(
            data={
                'first_name': test_first_name,
                'surname': test_surname,
                'card_number': test_card_number,
                'opening_balance': test_opening_balance,
            },
            existing_cards=existing_cards
        )
        self.assertFalse(form.is_valid())

    def test_opening_balance_is_negative(self):
        """The form rejects negative values"""
        # get test customer details
        cust_inst = Customer.objects.all()
        existing_cards = []
        for cust in cust_inst:
            existing_cards.append(cust.card_number)
        # test instance
        test_first_name = 'test'
        test_surname = 'test'
        test_card_number = 1
        test_opening_balance = Money(-1, customsettings.CURRENCY)
        form = CreateNewCustomerForm(
            data={
                'first_name': test_first_name,
                'surname': test_surname,
                'card_number': test_card_number,
                'opening_balance': test_opening_balance,
            },
            existing_cards=existing_cards
        )
        self.assertFalse(form.is_valid())
