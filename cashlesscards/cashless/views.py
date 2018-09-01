import datetime

from django.shortcuts import render
from django.db.models import Sum
from django.views import generic

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from djmoney.money import Money

from . import customsettings
from .models import Customer, Cash, Transaction
from .forms import AddCashForm, DeductCashForm
from .voucherhandler import apply_voucher, debit_voucher


def index(request):
    """Homepage for the cashless card system"""
    return render(request, 'index.html')


def info(request):
    """Displays general information about the site."""

    # Generate counts of some of the main objects
    num_customers = Customer.objects.all().count()
    num_cash = Cash.objects.all().count()

    # Total cash held in system
    sum_cash = Cash.objects.aggregate(Sum('cash_value'))['cash_value__sum']

    context = {
        'num_customers': num_customers,
        'num_cash': num_cash,
        'sum_cash': sum_cash,
    }

    # Render the HTML template info.html with the data in the context variable
    return render(request, 'cashless/info.html', context=context)


def search(request):
    """Simple search box to query card numbers"""
    query = request.GET.get('q')
    try:
        query = int(query)
    except ValueError:
        query = None
        results = None
    if query:
        results = Customer.objects.get(card_number=query)
        apply_voucher(results)
    return render(request, 'cashless/results.html', {"results": results,})


class CustomerDetailView(generic.DetailView):
    """Customer detail using the generic detail view"""
    model = Customer


@permission_required('cashless.can_transact')
def add_cash_cashier(request, pk):
    """View function for adding cash to a specific customer's account by cashier"""
    cash_inst = get_object_or_404(Cash, customer_id=pk)
    cash_inst.total = cash_inst.cash_value + cash_inst.voucher_value

    # if this is a POST request then process the Form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request (binding):
        form = AddCashForm(request.POST)

        # check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            clean_data = form.cleaned_data['cash_to_add']
            cash_inst.cash_value += clean_data
            # log transaction data
            credit = Transaction(
                customer_id=pk,
                transaction_type="credit",
                transaction_value=clean_data,
                )
            # write it to the model cash_value field
            cash_inst.save()
            credit.save()

            # redirect to a new URL:
            return HttpResponseRedirect(
                reverse('customer_detail', kwargs={'pk':cash_inst.customer_id})
                )

    # if this is a GET (or any other method) create the default form.
    else:
        proposed_cash_value = Money(5, customsettings.CURRENCY)
        form = AddCashForm(initial={'cash_to_add': proposed_cash_value,})

    return render(request, 'cashless/cash_transactions.html', {'form':form, 'cashinst':cash_inst})


@permission_required('cashless.can_transact')
def deduct_cash_cashier(request, pk):
    """View function for deducting cash from a specific customer's account by cashier"""
    cash_inst = get_object_or_404(Cash, customer_id=pk)
    cash_inst.total = cash_inst.cash_value + cash_inst.voucher_value

    # if this is a POST request then process the Form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request (binding):
        form = DeductCashForm(request.POST)

        # check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            clean_data = form.cleaned_data['cash_to_deduct']

            # check if amount to deduct is less than or equal to what customer has available
            if clean_data <= (cash_inst.cash_value + cash_inst.voucher_value):
                # conduct debit, debiting any vouchers first
                cash_inst, voucher_debit, cash_debit = debit_voucher(cash_inst, clean_data)
                # log transaction data
                debit = Transaction(
                    customer_id=pk,
                    transaction_type="debit",
                    transaction_value=cash_debit,
                    voucher_value=voucher_debit,
                    )
                # write it to the model cash_value field
                cash_inst.save()
                debit.save()

            # if amount to deduct is more than customer can afford
            else:
                # generate contextual message and default form
                message = True,
                proposed_cash_value = Money(5, customsettings.CURRENCY)
                form = DeductCashForm(initial={'cash_to_deduct': proposed_cash_value,})

                # Render the HTML template with the context variable
                return render(
                    request, 'cashless/cash_transactions.html', {
                        'form':form, 'cashinst':cash_inst, 'too_much':message
                    }
                    )

            # redirect to a new URL:
            return HttpResponseRedirect(
                reverse('customer_detail', kwargs={'pk':cash_inst.customer_id})
                )

    # if this is a GET (or any other method) create the default form.
    else:
        proposed_cash_value = Money(5, customsettings.CURRENCY)
        form = DeductCashForm(initial={'cash_to_deduct': proposed_cash_value,})

    return render(request, 'cashless/cash_transactions.html', {'form':form, 'cashinst':cash_inst})


class ActivityLog(PermissionRequiredMixin, generic.ListView):
    """Transaction log using the generic list view"""
    permission_required = 'cashless.view_finance'
    model = Transaction
    context_object_name = 'transaction_log'
    template_name = 'cashless/activity_log.html'

    def get_queryset(self):
        """Filter log down to records from just this year"""
        now = datetime.datetime.now()
        return Transaction.objects.filter(transaction_time__month=now.month)
