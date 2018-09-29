from datetime import timedelta, date
from django.test import TestCase
from djmoney.money import Money

from cashless import customsettings
from cashless.models import Voucher, Customer, Cash, VoucherLink
from cashless.voucherhandler import apply_voucher, debit_voucher


class ApplyVoucherHandlerTest(TestCase):
    """Tests the apply voucher function"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # create test models
        test_customer1 = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )
        test_cash1 = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_customer2 = Customer.objects.create(
            card_number=98,
            first_name='Jane',
            surname='Smith',
        )
        test_cash2 = Cash.objects.create(
            customer_id=2,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_customer3 = Customer.objects.create(
            card_number=97,
            first_name='Jenny',
            surname='Smith',
        )
        test_cash3 = Cash.objects.create(
            customer_id=3,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_voucher = Voucher.objects.create(
            voucher_application="daily",
            voucher_name="free breakfast",
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_link1 = VoucherLink.objects.create(
            customer_id=1,
            voucher_id=1,
            last_applied=date.today()-timedelta(days=1), # yesterday
        )
        test_link3 = VoucherLink.objects.create(
            customer_id=3,
            voucher_id=1,
            last_applied=date.today(),
        )
        test_customer1.save()
        test_cash1.save()
        test_customer2.save()
        test_cash2.save()
        test_customer3.save()
        test_cash3.save()
        test_voucher.save()
        test_link1.save()
        test_link3.save()

    def test_is_voucher_yesterday(self):
        """If customer eligible for a voucher and last voucher issued was yesterday"""
        test_customer = Customer.objects.get(pk=1)
        #test_link = VoucherLink.objects.get(customer_id=test_customer.pk)
        expected_result = Money(5, customsettings.CURRENCY)
        apply_voucher(test_customer)
        #self.assertEqual(test_link.last_applied, date.today())
        self.assertEqual(test_customer.cash.voucher_value, expected_result)

    def test_no_voucher(self):
        """If customer is not eligible for a voucher"""
        test_customer = Customer.objects.get(pk=2)
        expected_result = Money(5, customsettings.CURRENCY)
        apply_voucher(test_customer)
        self.assertEqual(test_customer.cash.voucher_value, expected_result)

    def test_is_voucher_today(self):
        """If customer eligible for a voucher and last voucher issued was today"""
        test_customer = Customer.objects.get(pk=3)
        test_link = VoucherLink.objects.get(customer_id=test_customer.pk)
        expected_result = Money(5, customsettings.CURRENCY)
        apply_voucher(test_customer)
        self.assertEqual(test_link.last_applied, date.today())
        self.assertEqual(test_customer.cash.voucher_value, expected_result)



class DebitVoucherTest(TestCase):
    """Tests the debit voucher function"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        test_cash1 = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_cash1.save()

    def test_value_more_than_voucher(self):
        """If the value to deduct is more than voucher"""
        # run preparation
        test_cash = Cash.objects.get(pk=1)
        test_value = Money(6, customsettings.CURRENCY)
        expected_cash_value = Money(1, customsettings.CURRENCY)
        expected_voucher_value = Money(0, customsettings.CURRENCY)
        expected_voucher_debit = Money(5, customsettings.CURRENCY)
        expected_cash_debit = Money(1, customsettings.CURRENCY)
        # run function
        cash, voucher_debit, cash_debit = debit_voucher(test_cash, test_value)
        # test output
        self.assertEqual(cash.cash_value, expected_cash_value)
        self.assertEqual(cash.voucher_value, expected_voucher_value)
        self.assertEqual(voucher_debit, expected_voucher_debit)
        self.assertEqual(cash_debit, expected_cash_debit)

    def test_value_less_than_voucher(self):
        """If the value to deduct is less than voucher"""
        # run preparation
        test_cash = Cash.objects.get(pk=1)
        test_value = Money(2, customsettings.CURRENCY)
        expected_cash_value = Money(2, customsettings.CURRENCY)
        expected_voucher_value = Money(3, customsettings.CURRENCY)
        expected_voucher_debit = Money(2, customsettings.CURRENCY)
        expected_cash_debit = Money(0, customsettings.CURRENCY)
        # run function
        cash, voucher_debit, cash_debit = debit_voucher(test_cash, test_value)
        # test output
        self.assertEqual(cash.cash_value, expected_cash_value)
        self.assertEqual(cash.voucher_value, expected_voucher_value)
        self.assertEqual(voucher_debit, expected_voucher_debit)
        self.assertEqual(cash_debit, expected_cash_debit)

    def test_value_is_equal_voucher(self):
        """If the value to deduct is equal to voucher"""
        # run preparation
        test_cash = Cash.objects.get(pk=1)
        test_value = Money(5, customsettings.CURRENCY)
        expected_cash_value = Money(2, customsettings.CURRENCY)
        expected_voucher_value = Money(0, customsettings.CURRENCY)
        expected_voucher_debit = Money(5, customsettings.CURRENCY)
        expected_cash_debit = Money(0, customsettings.CURRENCY)
        # run function
        cash, voucher_debit, cash_debit = debit_voucher(test_cash, test_value)
        # test output
        self.assertEqual(cash.cash_value, expected_cash_value)
        self.assertEqual(cash.voucher_value, expected_voucher_value)
        self.assertEqual(voucher_debit, expected_voucher_debit)
        self.assertEqual(cash_debit, expected_cash_debit)
