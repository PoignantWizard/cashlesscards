import datetime
from djmoney.money import Money

from . import customsettings
from .models import Cash, FreeMealValue, Transaction


def daily_fsm(customer):
    """Updates the voucher value if today is a new day"""
    fsm = 1
    voucher = FreeMealValue.objects.get(pk=fsm)
    cash_inst = Cash.objects.get(customer_id=customer.pk)

    # if customer eligible for free meals and voucher hasn't been updated today
    if customer.free_meals == fsm and cash_inst.voucher_date != datetime.date.today():
        # update cash balance
        cash_inst.voucher_value += voucher.meal_value
        cash_inst.voucher_date = datetime.date.today()
        cash_inst.save()

        # update transaction log
        transact = Transaction(
            customer_id=customer.pk,
            transaction_type="credit",
            voucher_value=voucher.meal_value,
        )
        transact.save()


def debit_voucher(cash, value):
    """Deducts cash from voucher if customer is eligible
    and returns remainder values"""
    # if value to debit is more than voucher
    if value > cash.voucher_value:
        # debit voucher
        voucher_debit = cash.voucher_value # amount to record in transaction log
        value -= cash.voucher_value
        cash.voucher_value = Money(0, customsettings.CURRENCY)
        # debit cash account
        cash_debit = value # amount to record in transaction log
        cash.cash_value -= value

    # if value to debit is less than or equal to voucher
    elif value <= cash.voucher_value:
        # debit voucher
        voucher_debit = value # amount to record in transaction log
        cash.voucher_value -= value
        # log for cash account
        cash_debit = Money(0, customsettings.CURRENCY)

    return cash, voucher_debit, cash_debit
