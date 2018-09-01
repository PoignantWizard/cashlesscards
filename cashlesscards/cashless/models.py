import datetime

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from djmoney.models.fields import MoneyField

from . import customsettings


class FreeMealValue(models.Model):
    """Lookup table to define the value of free meals vouchers"""
    meal_value = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=customsettings.CURRENCY,
        default=0
    )

    def __str__(self):
        """String for representing the Model object"""
        return "Free meal voucher value: " + str(self.meal_value)


class Customer(models.Model):
    """The user details table"""
    card_number = models.IntegerField()
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    FREE_STATUS = (
        (0, "Not eligible"),
        (1, "Eligible"),
    )

    free_meals = models.IntegerField(
        choices=FREE_STATUS,
        default=0,
        help_text="Select whether customer is eligible for free meals"
    )

    class Meta:
        """Declare model-level metadata to control default ordering of records and set plural"""
        ordering = ["surname", "first_name"]
        verbose_name_plural = "customers"
        permissions = (
            ("can_set_free_meals", "Set free meal eligibility"),
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
    voucher_date = models.DateField(default=datetime.date.today)

    class Meta:
        """Declare model-level metadata to set plural"""
        verbose_name_plural = "cash"
        permissions = (
            ("can_transact", "Conduct transactions"),
        )

    def __str__(self):
        """String for representing the Model object"""
        return "Customer's available cash: " + str(self.cash_value + self.voucher_value)


class Transaction(models.Model):
    """The transaction log table"""
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    transaction_time = models.DateTimeField(default=now, blank=True)

    credit = "credit"
    debit = "debit"
    transact_choices = (
        (credit, "Credit"),
        (debit, "Debit"),
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
        permissions = (
            ("view_finance", "Can view transaction log"),
        )

    #def __str__(self):
    #    """String for representing the Model object"""
    #    return Customer.first_name + " " + Customer.surname + " was " + transaction_type + "ed " \
    #        + str(self.transaction_value + self.voucher_value) \
    #        + " on " + str(self.transaction_time)
