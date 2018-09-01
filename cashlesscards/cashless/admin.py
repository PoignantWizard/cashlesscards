from django.contrib import admin
from .models import Customer, Cash, FreeMealValue


class CashInline(admin.StackedInline):
    """Customises the view of cash when inline"""
    model = Cash


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customises the customers admin page"""
    list_display = ("surname", "first_name", "free_meals")
    list_filter = ["free_meals"]
    fields = ["first_name", "surname", "free_meals", "card_number"]
    inlines = [CashInline]


@admin.register(FreeMealValue)
class FreeMealAdmin(admin.ModelAdmin):
    """Customises the free meals voucher admin page"""
    def has_add_permission(self, request):
        """Removes the add row permission"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Removes the delete row permission"""
        return False
