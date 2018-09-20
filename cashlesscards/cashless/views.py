import datetime

from django.shortcuts import render
from django.db.models import Sum
from django.views import generic

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from djmoney.money import Money

from . import customsettings
from .models import Customer, Cash, Transaction, VoucherLink, Voucher
from .forms import AddCashForm, DeductCashForm, AddVoucherLinkForm, CreateNewVoucherForm
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
        'version': customsettings.VERSION,
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
    paginate_by = 20
    context_object_name = 'transaction_log'
    template_name = 'cashless/activity_log.html'

    def get_queryset(self):
        """Filter log down to records from just this year"""
        now = datetime.datetime.now()
        return Transaction.objects.filter(transaction_time__month=now.month)


@permission_required('can_assign_voucher')
def add_voucher_link(request, pk):
    """View function for assigning a voucher to a specific customer's account"""
    link_inst = VoucherLink.objects.filter(customer_id=pk)
    custom_inst = Customer.objects.get(pk=pk)
    # get voucher details
    existing_vouchers = []
    for link in link_inst:
        existing_vouchers.append(link.voucher_id)

    # initialize form
    form = AddVoucherLinkForm(request.POST, existing_vouchers=existing_vouchers)

    if request.method == "POST":
        if form.is_valid():
            # process the input
            clean_data = form.cleaned_data['voucher']

            # assign voucher to customer's account
            new_voucher = VoucherLink(
                customer_id=int(pk),
                voucher_id=int(clean_data),
            )
            # write it to the model
            new_voucher.save()

            # redirect to a new URL:
            return HttpResponseRedirect(
                reverse('customer_detail', kwargs={'pk':pk})
                )

    # if this is a GET (or any other method) create the default form.
    else:
        proposed_voucher = 1
        form = AddVoucherLinkForm(
            initial={
                'voucher': proposed_voucher,
            },
            existing_vouchers=existing_vouchers
        )

    return render(request, 'cashless/assign_voucher.html', {
        'form':form,
        'custom_inst':custom_inst,
        'link_inst':link_inst,
    })


@permission_required('can_add_vouchers')
def create_new_voucher(request):
    """View function for creating a new voucher"""
    vouch_inst = Voucher.objects.all()
    # get voucher details
    existing_vouchers = []
    for vouch in vouch_inst:
        existing_vouchers.append(vouch.voucher_name)

    # initialize form
    form = CreateNewVoucherForm(request.POST, existing_vouchers=existing_vouchers)

    if request.method == "POST":
        if form.is_valid():
            # process the input
            clean_application = form.cleaned_data['application']
            clean_name = form.cleaned_data['name']
            clean_value = form.cleaned_data['value']

            # build new voucher ready for model
            new_voucher = Voucher(
                voucher_application=clean_application,
                voucher_name=clean_name,
                voucher_value=clean_value,
            )
            # write it to the model
            new_voucher.save()

            # redirect to a new URL
            return HttpResponseRedirect(
                reverse('voucher_detail')
            )

    # if this is a GET (or any other method) create the default form.
    else:
        proposed_application = "daily"
        proposed_name = ""
        proposed_value = Money(5, customsettings.CURRENCY)
        form = CreateNewVoucherForm(
            initial={
                'application': proposed_application,
                'name': proposed_name,
                'value': proposed_value,
            },
            existing_vouchers=existing_vouchers
        )

    return render(request, 'cashless/new_voucher.html', {
        'form':form,
    })


class VoucherListView(PermissionRequiredMixin, generic.ListView):
    """A list of all vouchers using the generic list view"""
    permission_required = 'cashless.can_add_vouchers'
    model = Voucher
    paginate_by = 20


class VoucherDetailView(PermissionRequiredMixin, generic.DetailView):
    """Voucher detail using the generic detail view"""
    permission_required = 'cashless.can_add_vouchers'
    model = Voucher


class VoucherUpdate(PermissionRequiredMixin, UpdateView):
    """Voucher update form using the generic view"""
    permission_required = 'cashless.can_add_vouchers'
    model = Voucher
    fields = [
        'voucher_application',
        'voucher_name',
        'voucher_value'
    ]
    template_name_suffix = '_handler'


class VoucherDelete(PermissionRequiredMixin, DeleteView):
    """Voucher delete form using the generic view"""
    permission_required = 'cashless.can_add_vouchers'
    model = Voucher
    success_url = reverse_lazy('voucher_list')


#class AuthorCreate(CreateView):
#    model = Author
#    fields = '__all__'
#    initial = {'date_of_death': '05/01/2018'}
