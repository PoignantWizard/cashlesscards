import datetime
import time
from djmoney.money import Money

from . import customsettings
from .models import VoucherLink, Voucher, Transaction


def apply_voucher(customer):
    """Updates the voucher value if haven't already this time period"""
    # get associated records
    voucher_list = VoucherLink.objects.filter(customer_id=customer.pk)
    cash_inst = customer.cash
    today = datetime.date.today()

    # loop through customer's vouchers
    for v in voucher_list:
        v_inst = Voucher.objects.get(pk=v.voucher_id)

        # utility values
        lw = time.strptime(str(v.last_applied), "%Y-%m-%d")
        tw = time.strptime(str(today), "%Y-%m-%d")
        last_week = time.strftime("%W", lw)
        today_week = time.strftime("%W", tw)

        # check it's appropriate to apply voucher to customer's account
        if (v_inst.voucher_application == "daily" and v.last_applied != today) \
            or (v_inst.voucher_application == "weekly" and last_week != today_week) \
            or (v_inst.voucher_application == "monthly" and v.last_applied.month != today.month) \
            or (v_inst.voucher_application == "yearly" and v.last_applied.year != today.year):

            # update cash balance
            cash_inst.voucher_value += v_inst.voucher_value
            cash_inst.save()
            v.last_applied = today
            v.save()

            # update transaction log
            transact = Transaction(
                customer_id=customer.pk,
                transaction_type="credit",
                voucher_value=v_inst.voucher_value,
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
