import datetime

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from djmoney.models.fields import MoneyField

from . import customsettings


class Voucher(models.Model):
    """Lookup table to define available vouchers and their values"""

    voucher_application = models.CharField(
        max_length=255,
        choices=customsettings.TIMING,
        default="daily",
        help_text="Select how often the voucher is applied to the customer's account"
    )
    voucher_name = models.CharField(max_length=255)
    voucher_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0
    )

    class Meta:
        """Declare model-level metadata"""
        ordering = ["voucher_name"]
        default_permissions = ()
        permissions = (
            ("can_add_vouchers", "Create and edit vouchers"),
        )

    def __str__(self):
        """String for representing the Model object"""
        return self.voucher_name + ": " + str(self.voucher_value)


class Customer(models.Model):
    """The customer details table"""
    card_number = models.IntegerField()
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    class Meta:
        """Declare model-level metadata to control default ordering of records and set plural"""
        ordering = ["surname", "first_name"]
        verbose_name_plural = "customers"
        default_permissions = ()
        permissions = (
            ("can_add_customers", "Create and edit customer accounts"),
        )

    def __str__(self):
        """String for representing the Model object"""
        return self.first_name + " " + self.surname

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Customer"""
        return reverse('customer_detail', args=[str(self.id)])

    def get_absolute_url_loggedin(self):
        """Returns the url to access a particular instance of Customer"""
        return reverse('customer_detail_loggedin', args=[str(self.id)])


class Cash(models.Model):
    """The cash store table"""
    customer = models.OneToOneField(Customer, related_name='cash', on_delete=models.CASCADE)
    cash_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0
    )
    voucher_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0,
    )

    class Meta:
        """Declare model-level metadata to set plural"""
        verbose_name_plural = "cash"
        default_permissions = ()
        permissions = (
            ("can_transact", "Conduct transactions"),
        )

    def __str__(self):
        """String for representing the Model object"""
        return "Customer's available cash: " + str(self.cash_value + self.voucher_value)


class VoucherLink(models.Model):
    """Lists each customer's vouchers and when they were last applied"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)

    last_year = datetime.datetime.now() - datetime.timedelta(days=365)

    last_applied = models.DateField(default=last_year)
    voucher_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0,
    )

    class Meta:
        """Declare model-level metadata"""
        default_permissions = ()
        permissions = (
            ("can_assign_voucher", "Assign vouchers to customers"),
        )


class Transaction(models.Model):
    """The transaction log table"""
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    transaction_time = models.DateTimeField(default=now, blank=True)

    credit = "credit"
    debit = "debit"
    stripe = "stripe"
    transact_choices = (
        (credit, "Credit"),
        (debit, "Debit"),
        (stripe, "Stripe Credit"),
    )

    transaction_type = models.CharField(
        max_length=6,
        choices=transact_choices,
        default=credit
    )
    transaction_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0
    )
    voucher_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0
    )

    class Meta:
        """Declare model-level metadata to control default ordering of records and set plural"""
        ordering = ["-transaction_time"]
        verbose_name_plural = "transactions"
        default_permissions = ()
        permissions = (
            ("view_finance", "Can view transaction log"),
        )
