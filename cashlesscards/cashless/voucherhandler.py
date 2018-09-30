import datetime
import time
from djmoney.money import Money

from . import customsettings
from .models import VoucherLink, Voucher, Transaction, Cash


def apply_voucher(customer):
    """Resets the voucher value if haven't already this time period"""
    # get associated records
    voucher_list = VoucherLink.objects.filter(customer_id=customer.pk)
    cash_inst = Cash.objects.get(customer_id=customer.pk)
    today = datetime.date.today()
    value = 0
    check = False

    # if customer has any vouchers assigned
    if voucher_list:
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
                or (v_inst.voucher_application == "monthly" \
                                        and v.last_applied.month != today.month) \
                or (v_inst.voucher_application == "yearly" and v.last_applied.year != today.year):

                # define checker value
                check = True

                # update voucher value
                v.voucher_value = v_inst.voucher_value
                v.last_applied = today
                v.save()

            # add voucher value to total
            value += v.voucher_value


    if check:
        # update cash balance
        transact_value = value - cash_inst.voucher_value
        cash_inst.voucher_value = value
        cash_inst.save()

        # update transaction log
        transact = Transaction(
            customer_id=customer.pk,
            transaction_type="credit",
            voucher_value=transact_value,
        )
        transact.save()


def debit_voucher(cash, value):
    """Deducts cash from voucher if customer is eligible
    and returns remainder values"""
    # distribute debit across vouchers so resetting doesn't wipe over remaining value
    distribute_voucher_debit(cash, value)

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


def distribute_voucher_debit(cash, value):
    """Deducts the value from each linked voucher so
    regular resets maintain values"""
    voucher_list = VoucherLink.objects.filter(customer_id=cash.customer_id)
    # if value is more than zero
    if value > Money(0, customsettings.CURRENCY):
        # if customer has any vouchers assigned
        if voucher_list:
            # loop through customer's vouchers
            for v in voucher_list:

                # if value to debit is more than selected voucher
                if value > v.voucher_value:
                    # debit voucher
                    value -= v.voucher_value
                    v.voucher_value = Money(0, customsettings.CURRENCY)
                    v.save()

                # if value to debit is less than or equal to voucher
                elif value <= v.voucher_value:
                    # debit voucher
                    v.voucher_value -= value
                    v.save()
                    value = Money(0, customsettings.CURRENCY)
