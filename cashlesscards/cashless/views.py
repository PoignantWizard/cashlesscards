import datetime
import stripe

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.views import generic
from django.conf import settings

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from djmoney.money import Money

from . import customsettings
from .models import Customer, Cash, Transaction, VoucherLink, Voucher
from .forms import AddCashForm, DeductCashForm, AddCashForStripePaymentForm
from .forms import AddVoucherLinkForm, RemoveVoucherLinkForm
from .forms import CreateNewVoucherForm, CreateNewCustomerForm
from .voucherhandler import apply_voucher, debit_voucher
from .updates import check_current_version


stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    """Homepage for the cashless card system"""
    return render(request, 'index.html')


def info(request):
    """Displays general information about the site."""

    # Generate counts of some of the main objects
    num_customers = Customer.objects.all().count()
    num_cash = Cash.objects.all().count()

    # Total cash held in system set to correct format
    sum_cash = Cash.objects.aggregate(Sum('cash_value'))['cash_value__sum']
    sum_cash = str("{:.2f}".format(sum_cash))

    # check current version if possible
    try:
        version_match, git_version = check_current_version()
        update_message = "Version " + str(git_version) + " is available."
    except:
        version_match = False
        update_message = "Unable to check for updates."

    context = {
        'version': customsettings.VERSION,
        'version_match': version_match,
        'update_message': update_message,
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
    try:
        if query:
            results = Customer.objects.get(card_number=query)
            apply_voucher(results)
            cash_inst = Cash.objects.get(customer_id=results.pk)
            results.total_balance = cash_inst.cash_value + cash_inst.voucher_value
    except:
        results = None
    return render(request, 'cashless/results.html', {"results": results,})


class CustomerDetailView(generic.DetailView):
    """Customer detail using the generic detail view"""
    model = Customer

    def get_context_data(self, **kwargs):
        """override context data defaults"""
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        total_balance = self.get_total_balance()
        context['total_balance'] = total_balance
        return context

    def get_total_balance(self):
        """calculate the customer's total balance"""
        pk = self.kwargs.get('pk')
        cash_inst = Cash.objects.get(customer_id=pk)
        total_balance = cash_inst.cash_value + cash_inst.voucher_value
        return total_balance


def customer_payment(request, pk):
    """Get cash amount to add to account and handle card payment"""
    cash_inst = get_object_or_404(Cash, customer_id=pk)
    cash_inst.total = cash_inst.cash_value + cash_inst.voucher_value

    if request.method == 'POST':
        form = AddCashForStripePaymentForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            clean_data = form.cleaned_data['cash_to_add']
            stripe_amount = int(clean_data.amount * 100)

            # send stripe.js card payment (avoiding storing any card details)
            charge = stripe.Charge.create(
                amount=stripe_amount,
                currency=customsettings.CURRENCY,
                description='Add cash to account',
                source=request.POST['stripeToken']
            )

            if charge['status'] == 'succeeded':
                cash_inst.cash_value += clean_data
                # log transaction data
                credit = Transaction(
                    customer_id=pk,
                    transaction_type="stripe",
                    transaction_value=clean_data,
                    )
                # write it to the model cash_value field
                cash_inst.save()
                credit.save()

            # render success confirmation page
            total_balance = cash_inst.cash_value + cash_inst.voucher_value
            return render(
                request,
                'cashless/customer_charged.html',
                {
                    'key': settings.STRIPE_PUBLISHABLE_KEY,
                    'cash_amount': clean_data,
                    'stripe_amount': stripe_amount,
                    'cashinst': cash_inst,
                    'total': total_balance,
                }
            )

    # if this is a GET (or any other method) create the default form.
    else:
        proposed_cash_value = Money(5, customsettings.CURRENCY)
        form = AddCashForStripePaymentForm(
            initial={'cash_to_add': proposed_cash_value,}
        )
    return render(
        request,
        'cashless/customer_payment.html',
        {
            'form': form,
            'cashinst': cash_inst,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
        }
    )


def customer_charged(request, pk):
    """Return confirmation of stripe.js payment to customer"""
    return render(
        request,
        'cashless/customer_charged.html',
        {
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'cash_amount': request.POST['cash_amount'],
            'stripe_amount': request.POST['stripe_amount'],
            'cashinst': request.POST['cash_inst'],
            'total': request.POST['total'],
        }
    )


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
                message = True
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


@permission_required('cashless.can_assign_voucher')
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

            # redirect to a new URL
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

    return render(request, 'cashless/voucher_assign.html', {
        'form':form,
        'custom_inst':custom_inst,
        'link_inst':link_inst,
    })


@permission_required('cashless.can_assign_voucher')
def remove_voucher_link(request, pk, voucher_id):
    """View function for unassigning a voucher from a specific customer's account"""
    link_inst = VoucherLink.objects.get(customer_id=pk, voucher_id=voucher_id)
    custom_inst = Customer.objects.get(pk=pk)

    # initialise form
    form = RemoveVoucherLinkForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            delete_voucher = form.cleaned_data['delete_voucher']
            if delete_voucher is True:
                # delete the voucher
                link_inst.delete()

                # redirect to a new URL
                return HttpResponseRedirect(
                    reverse('customer_detail', kwargs={'pk':pk})
                )

    # if this is a GET (or any other method) create the default form
    else:
        proposed_value = False
        form = RemoveVoucherLinkForm(
            initial={'delete_voucher': proposed_value}
        )

    return render(request, 'cashless/voucher_unassign.html', {
        'form':form,
        'custom_inst':custom_inst,
    })


@permission_required('cashless.can_add_vouchers')
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
                reverse('voucher_detail', kwargs={'pk':new_voucher.pk})
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

    return render(request, 'cashless/voucher_new.html', {
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
    success_url = reverse_lazy('voucher_list')


class VoucherDelete(PermissionRequiredMixin, DeleteView):
    """Voucher delete form using the generic view"""
    permission_required = 'cashless.can_add_vouchers'
    model = Voucher
    success_url = reverse_lazy('voucher_list')


@permission_required('cashless.can_add_customers')
def create_new_customer(request):
    """View function for creating a new voucher"""
    # get customer details
    cust_inst = Customer.objects.all()
    existing_cards = []
    for cust in cust_inst:
        existing_cards.append(cust.card_number)

    # initialize form
    form = CreateNewCustomerForm(request.POST, existing_cards=existing_cards)

    if request.method == "POST":
        if form.is_valid():
            # process the input
            clean_first_name = form.cleaned_data['first_name']
            clean_surname = form.cleaned_data['surname']
            clean_card_number = form.cleaned_data['card_number']
            clean_opening_balance = form.cleaned_data['opening_balance']

            # build new customer and write to model
            new_customer = Customer(
                card_number=clean_card_number,
                first_name=clean_first_name,
                surname=clean_surname,
            )
            new_customer.save()

            # build new cash account and write to model
            new_cash = Cash(
                customer_id=new_customer.pk,
                cash_value=clean_opening_balance,
            )
            new_cash.save()

            # build new transaction record and write to model
            new_transaction = Transaction(
                customer_id=new_customer.pk,
                transaction_type="credit",
                transaction_value=clean_opening_balance,
            )
            new_transaction.save()

            # redirect to a new URL
            return HttpResponseRedirect(
                reverse('customer_detail', kwargs={'pk':new_customer.pk})
            )

    # if this is a GET (or any other method) create the default form.
    else:
        proposed_first_name = ""
        proposed_surname = ""
        proposed_card_number = ""
        proposed_opening_balance = Money(0, customsettings.CURRENCY)
        form = CreateNewCustomerForm(
            initial={
                'first_name': proposed_first_name,
                'surname': proposed_surname,
                'card_number': proposed_card_number,
                'opening_balance': proposed_opening_balance,
            },
            existing_cards=existing_cards
        )

    return render(request, 'cashless/customer_new.html', {
        'form':form,
    })


class CustomerListView(PermissionRequiredMixin, generic.ListView):
    """A list of all customers using the generic list view"""
    permission_required = 'cashless.can_add_customers'
    model = Customer
    paginate_by = 20


class CustomerUpdate(PermissionRequiredMixin, UpdateView):
    """Customer update form using the generic view"""
    permission_required = 'cashless.can_add_customers'
    model = Customer
    fields = [
        'card_number',
        'first_name',
        'surname'
    ]
    template_name_suffix = '_handler'
    success_url = reverse_lazy('customer_list')


class CustomerDelete(PermissionRequiredMixin, DeleteView):
    """Customer delete form using the generic view"""
    permission_required = 'cashless.can_add_customer'
    model = Customer
    success_url = reverse_lazy('customer_list')


class ActivityLog(PermissionRequiredMixin, generic.ListView):
    """Transaction log using the generic list view"""
    permission_required = 'cashless.view_finance'
    model = Transaction
    paginate_by = 10
    context_object_name = 'transaction_log'
    template_name = 'cashless/activity_log.html'

    def get_queryset(self):
        """Filter log down to records from just this year"""
        now = datetime.datetime.now()
        return Transaction.objects.filter(transaction_time__month=now.month)


class ActivityLogToCsv(ActivityLog):
    """Subclass of activity log that produces a CSV file"""
    template_name = 'cashless/activitylog.csv'
    content_type = 'text/csv'
