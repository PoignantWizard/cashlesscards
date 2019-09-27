import datetime
from django.test import TestCase
from django.utils.timezone import now
from djmoney.money import Money

from cashless import customsettings
from cashless.models import Voucher, Customer, Cash, VoucherLink, Transaction


class VoucherModelTest(TestCase):
    """Tests the Voucher model"""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        Voucher.objects.create(
            voucher_application="daily",
            voucher_name="Free breakfast",
            voucher_value=Money(2, customsettings.CURRENCY),
        )

    def test_voucher_application_label(self):
        """The verbose name of the voucher application field is as expected"""
        voucher = Voucher.objects.get(id=1)
        field_label = voucher._meta.get_field('voucher_application').verbose_name
        self.assertEqual(field_label, 'voucher application')

    def test_voucher_application_max_length(self):
        """The maximum length of the voucher application is as expected"""
        voucher = Voucher.objects.get(id=1)
        max_length = voucher._meta.get_field('voucher_application').max_length
        self.assertEqual(max_length, 255)

    def test_voucher_name_label(self):
        """The verbose name of the voucher name field is as expected"""
        voucher = Voucher.objects.get(id=1)
        field_label = voucher._meta.get_field('voucher_name').verbose_name
        self.assertEqual(field_label, 'voucher name')

    def test_voucher_name_max_length(self):
        """The maximum length of the voucher name is as expected"""
        voucher = Voucher.objects.get(id=1)
        max_length = voucher._meta.get_field('voucher_name').max_length
        self.assertEqual(max_length, 255)

    def test_voucher_value_label(self):
        """The verbose name of the voucher value field is as expected"""
        voucher = Voucher.objects.get(id=1)
        field_label = voucher._meta.get_field('voucher_value').verbose_name
        self.assertEqual(field_label, 'voucher value')

    def test_voucher_value_max_digits(self):
        """The maximum number of digits in the money value is as expected"""
        voucher = Voucher.objects.get(id=1)
        max_digits = voucher._meta.get_field('voucher_value').max_digits
        self.assertEqual(max_digits, 14)

    def test_object_name_is_voucher_value(self):
        """The string for representing the model object is as expected"""
        voucher = Voucher.objects.get(id=1)
        expected_object_name = f'{voucher.voucher_name}: {voucher.voucher_value}'
        self.assertEqual(expected_object_name, str(voucher))


class CustomerModelTest(TestCase):
    """Tests the Customer model"""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )

    def test_first_name_max_length(self):
        """The maximum length of the first name is as expected"""
        cust = Customer.objects.get(id=1)
        max_length = cust._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 255)

    def test_surname_max_length(self):
        """The maximum length of the surname is as expected"""
        cust = Customer.objects.get(id=1)
        max_length = cust._meta.get_field('surname').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_first_name_space_surname(self):
        """The string for representing the model object is as expected"""
        cust = Customer.objects.get(id=1)
        expected_object_name = f'{cust.first_name} {cust.surname}'
        self.assertEqual(expected_object_name, str(cust))

    def test_get_absolute_url(self):
        """The url to access a particular instance of Customer"""
        cust = Customer.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(cust.get_absolute_url(), '/cashless/customer/1')


class CashModelTest(TestCase):
    """Tests the Cash model"""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )

    def test_cash_value_max_digits(self):
        """The maximum number of digits in the cash value is as expected"""
        balance = Cash.objects.get(id=1)
        max_digits = balance._meta.get_field('cash_value').max_digits
        self.assertEqual(max_digits, 14)

    def test_voucher_value_max_digits(self):
        """The maximum number of digits in the voucher value is as expected"""
        balance = Cash.objects.get(id=1)
        max_digits = balance._meta.get_field('voucher_value').max_digits
        self.assertEqual(max_digits, 14)

    def test_object_name_is_total_balance(self):
        """The string for representing the model object is as expected"""
        balance = Cash.objects.get(id=1)
        total_balance = str(balance.cash_value + balance.voucher_value)
        expected_object_name = f'Customer\'s available cash: {total_balance}'
        self.assertEqual(expected_object_name, str(balance))


class VoucherLinkModelTest(TestCase):
    """Tests the VoucherLink model"""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        VoucherLink.objects.create(
            customer_id=1,
            voucher_id=1,
            last_applied=datetime.date.today(),
            voucher_value=Money(5, customsettings.CURRENCY),
        )

    def test_last_applied(self):
        """The last applied date is reset to today's date"""
        link = VoucherLink.objects.get(id=1)
        today = datetime.date.today()
        self.assertEqual(today, link.last_applied)

    def test_voucher_value_max_digits(self):
        """The maximum number of digits in the voucher value is as expected"""
        balance = VoucherLink.objects.get(id=1)
        max_digits = balance._meta.get_field('voucher_value').max_digits
        self.assertEqual(max_digits, 14)


class TransactionModelTest(TestCase):
    """Tests the Transaction model"""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        Transaction.objects.create(
            customer_id=1,
            transaction_time=now(),
            transaction_type='credit',
            transaction_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )

    def test_transaction_value_max_digits(self):
        """The maximum number of digits in the transaction value is as expected"""
        balance = Transaction.objects.get(id=1)
        max_digits = balance._meta.get_field('transaction_value').max_digits
        self.assertEqual(max_digits, 14)

    def test_transaction_voucher_value_max_digits(self):
        """The maximum number of digits in the transaction voucher value is as expected"""
        balance = Transaction.objects.get(id=1)
        max_digits = balance._meta.get_field('voucher_value').max_digits
        self.assertEqual(max_digits, 14)

    def test_transaction_status(self):
        """The transaction type is credit or debit or stripe.js payment"""
        balance = Transaction.objects.get(id=1)
        transact_choices = ['credit', 'debit', 'stripe']
        self.assertIn(balance.transaction_type, transact_choices)
