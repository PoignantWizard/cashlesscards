from datetime import timedelta, date
from django.test import TestCase
from djmoney.money import Money

from cashless import customsettings
from cashless.models import Customer, Cash, FreeMealValue
from cashless.voucherhandler import daily_fsm, debit_voucher


class DailyFsmHandlerTest(TestCase):
    """Tests the daily fsm function"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # find yesterday
        yesterday = date.today() - timedelta(days=1)
        # create test models
        test_customer1 = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
            free_meals=1,
        )
        test_cash1 = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
            voucher_date=yesterday,
        )
        test_customer2 = Customer.objects.create(
            card_number=98,
            first_name='Jane',
            surname='Smith',
            free_meals=0,
        )
        test_cash2 = Cash.objects.create(
            customer_id=2,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
            voucher_date=yesterday
        )
        test_customer3 = Customer.objects.create(
            card_number=97,
            first_name='Jenny',
            surname='Smith',
            free_meals=1,
        )
        test_cash3 = Cash.objects.create(
            customer_id=3,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
            voucher_date=date.today()
        )
        test_fsm = FreeMealValue.objects.create(
            meal_value=Money(5, customsettings.CURRENCY)
        )
        test_customer1.save()
        test_cash1.save()
        test_customer2.save()
        test_cash2.save()
        test_customer3.save()
        test_cash3.save()
        test_fsm.save()

    def test_is_fsm_voucher_yesterday(self):
        """If customer eligible for free meals and last voucher issued was yesterday"""
        test_customer = Customer.objects.get(pk=1)
        expected_result = Money(10, customsettings.CURRENCY)
        daily_fsm(test_customer)
        self.assertEqual(test_customer.cash.voucher_date, date.today())
        self.assertEqual(test_customer.cash.voucher_value, expected_result)

    def test_not_fsm(self):
        """If customer is not eligible for free meals"""
        test_customer = Customer.objects.get(pk=2)
        yesterday = date.today() - timedelta(days=1)
        expected_result = Money(5, customsettings.CURRENCY)
        daily_fsm(test_customer)
        self.assertEqual(test_customer.cash.voucher_date, yesterday)
        self.assertEqual(test_customer.cash.voucher_value, expected_result)

    def test_is_fsm_voucher_today(self):
        """If customer eligible for free meals and last voucher issued was today"""
        test_customer = Customer.objects.get(pk=3)
        expected_result = Money(5, customsettings.CURRENCY)
        daily_fsm(test_customer)
        self.assertEqual(test_customer.cash.voucher_date, date.today())
        self.assertEqual(test_customer.cash.voucher_value, expected_result)



class DebitVoucherTest(TestCase):
    """Tests the debit voucher function"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        test_cash1 = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
            voucher_date=date.today(),
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
