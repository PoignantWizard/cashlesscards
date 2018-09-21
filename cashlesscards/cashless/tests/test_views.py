from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils.timezone import now
from djmoney.money import Money

from cashless import customsettings
from cashless.models import Voucher, Customer, Cash, Transaction


class IndexViewTest(TestCase):
    """Tests the index view"""
    def test_view_url_exists_at_desired_location(self):
        """The URL exists in the expected location"""
        response = self.client.get('/cashless/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """The URL is accessible with a reverse lookup"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """The view uses the expected template"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class InfoViewTest(TestCase):
    """Tests the info view"""
    def test_view_url_exists_at_desired_location(self):
        """The URL exists in the expected location"""
        response = self.client.get('/cashless/info')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """The URL is accessible with a reverse lookup"""
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """The view uses the expected template"""
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashless/info.html')


class SearchViewTest(TestCase):
    """Tests the search view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        test_voucher = Voucher.objects.create(
            voucher_application="daily",
            voucher_name="free breakfast",
            voucher_value=Money(2, customsettings.CURRENCY),
        )
        test_customer = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )
        test_cash = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_voucher.save()
        test_customer.save()
        test_cash.save()

    def test_view_url_exists_at_desired_location(self):
        """The URL exists in the expected location"""
        response = self.client.get('/cashless/search/?q=99')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """The URL is accessible with a reverse lookup"""
        test_card_id = 99
        response = self.client.get(reverse('search'), {'q':test_card_id})
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """The view uses the expected template"""
        test_card_id = 99
        response = self.client.get(reverse('search'), {'q':test_card_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashless/results.html')


class ActivityLogViewTest(TestCase):
    """Tests the activity log view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create two users
        test_user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK',
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
        )
        # Add permissions
        permission = Permission.objects.get(name='Can view transaction log')
        test_user1.user_permissions.add(permission)
        test_user1.save()
        test_user2.save()

        # Create a transaction
        balance = Transaction.objects.create(
            customer_id=1,
            transaction_time=now(),
            transaction_type='credit',
            transaction_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        balance.save()

    def test_redirect_if_not_logged_in(self):
        """The view will redirect to a login page if the user is not logged in"""
        response = self.client.get(reverse('activity_log'))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/log')

    def test_redirect_if_user_not_permitted(self):
        """The view will redirect if the user doesn't have permisssions"""
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('activity_log'))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/log')

    def test_logged_in_uses_correct_template(self):
        """The page is displayed for a logged in user with permission"""
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('activity_log'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'cashless/activity_log.html')

    def test_transaction_log(self):
        """The context is the transaction log"""
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/cashless/log')
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check that we pick up transaction data
        self.assertTrue('transaction_log' in response.context)


class AddCashCashierViewTest(TestCase):
    """Tests the add cash cashier view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK',
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
        )
        # Add permisssions
        permission = Permission.objects.get(name='Conduct transactions')
        test_user1.user_permissions.add(permission)
        test_user1.save()
        test_user2.save()

        # Create a customer with cash account
        test_customer = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )
        test_cash = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_customer.save()
        test_cash.save()

    def test_redirect_if_not_logged_in(self):
        """The view will redirect to a login page if the user is not logged in"""
        test_customer = Customer.objects.get(id=1)
        response = self.client.get(reverse('add_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/' \
            + str(test_customer.pk) + '/addcash/')

    def test_redirect_if_user_not_permitted(self):
        """The view will redirect if the user doesn't have permisssions"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('add_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/' \
            + str(test_customer.pk) + '/addcash/')

    def test_logged_in_with_permission(self):
        """The page is displayed for a logged in user with permission"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_http404_for_invalid_customer_if_logged_in(self):
        """A 404 error is displayed if logged in but customer is not valid"""
        test_id = 99
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add_cash_cashier', \
            kwargs={'pk': test_id}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        """The view uses the expected template"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashless/cash_transactions.html')


class DeductCashCashierViewTest(TestCase):
    """Tests the deduct cash cashier view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK',
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
        )
        # Add permisssions
        permission = Permission.objects.get(name='Conduct transactions')
        test_user1.user_permissions.add(permission)
        test_user1.save()
        test_user2.save()

        # Create a customer with cash account
        test_customer = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )
        test_cash = Cash.objects.create(
            customer_id=1,
            cash_value=Money(2, customsettings.CURRENCY),
            voucher_value=Money(5, customsettings.CURRENCY),
        )
        test_customer.save()
        test_cash.save()

    def test_redirect_if_not_logged_in(self):
        """The view will redirect to a login page if the user is not logged in"""
        test_customer = Customer.objects.get(id=1)
        response = self.client.get(reverse('deduct_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/' \
            + str(test_customer.pk) + '/deductcash/')

    def test_redirect_if_user_not_permitted(self):
        """The view will redirect if the user doesn't have permisssions"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('deduct_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/' \
            + str(test_customer.pk) + '/deductcash/')

    def test_logged_in_with_permission(self):
        """The page is displayed for a logged in user with permission"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('deduct_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_http404_for_invalid_customer_if_logged_in(self):
        """A 404 error is displayed if logged in but customer is not valid"""
        test_id = 99
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('deduct_cash_cashier', \
            kwargs={'pk': test_id}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        """The view uses the expected template"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('deduct_cash_cashier', \
            kwargs={'pk': test_customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashless/cash_transactions.html')


class AddVoucherLinkViewTest(TestCase):
    """Tests the add voucher link view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK',
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
        )
        # Add permisssions
        permission = Permission.objects.get(name='Assign vouchers to customers')
        test_user1.user_permissions.add(permission)
        test_user1.save()
        test_user2.save()

        # Create a customer
        test_customer = Customer.objects.create(
            card_number=99,
            first_name='John',
            surname='Smith',
        )
        test_customer.save()

    def test_redirect_if_not_logged_in(self):
        """The view will redirect to a login page if the user is not logged in"""
        test_customer = Customer.objects.get(id=1)
        response = self.client.get(reverse('add_voucher_link', \
            kwargs={'pk': test_customer.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/' \
            + str(test_customer.pk) + '/assignvoucher/')

    def test_redirect_if_user_not_permitted(self):
        """The view will redirect if the user doesn't have permisssions"""
        test_customer = Customer.objects.get(id=1)
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('add_voucher_link', \
            kwargs={'pk': test_customer.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/' \
            + str(test_customer.pk) + '/assignvoucher/')


class CreateNewVoucherViewTest(TestCase):
    """Tests the create new voucher view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK',
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
        )
        # Add permisssions
        permission = Permission.objects.get(name='Create and edit vouchers')
        test_user1.user_permissions.add(permission)
        test_user1.save()
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        """The view will redirect to a login page if the user is not logged in"""
        response = self.client.get(reverse('create_new_voucher'))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/voucher/new')

    def test_redirect_if_user_not_permitted(self):
        """The view will redirect if the user doesn't have permisssions"""
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('create_new_voucher'))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/voucher/new')


class CreateNewCustomerViewTest(TestCase):
    """Tests the create new customer view"""
    def setUp(self):
        """Set up non-modified objects used by all test methods"""
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK',
        )
        test_user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD',
        )
        # Add permisssions
        permission = Permission.objects.get(name='Create and edit customer accounts')
        test_user1.user_permissions.add(permission)
        test_user1.save()
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        """The view will redirect to a login page if the user is not logged in"""
        response = self.client.get(reverse('create_new_customer'))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/new')

    def test_redirect_if_user_not_permitted(self):
        """The view will redirect if the user doesn't have permisssions"""
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('create_new_customer'))
        self.assertRedirects(response, '/accounts/login/?next=/cashless/customer/new')
