from django.contrib import admin
from .models import Customer, Cash, Voucher, VoucherLink


class CashInline(admin.StackedInline):
    """Customises the view of cash when inline"""
    model = Cash
    exclude = ["voucher_value"]


class VoucherLinkInline(admin.StackedInline):
    """Customises the list of vouchers when inline"""
    model = VoucherLink
    exclude = ["voucher_value"]
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customises the customers admin page"""
    list_display = ("surname", "first_name")
    fields = ["first_name", "surname", "card_number"]
    inlines = [CashInline, VoucherLinkInline]


admin.site.register(Voucher)
