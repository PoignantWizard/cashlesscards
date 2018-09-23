# Cashless cards system

A system designed to provide a cashless service in a "closed" environment, 
such as offices, clinics, and schools. 

Cashless cards is a web app that allows you to manage quick and simple 
transactions using NFC capable ID cards. After creating an account for a 
customer (including their card number), you can credit their account. 
Enter the customer's card number into the search box on the home page 
using a USB card reader. This will redirect you to their account. You can 
then debit their account when they purchase items or services within your 
closed environment. 

Cashless cards is also equipped with a powerful voucher service. Set the 
timing on a voucher to specify how often the value is credited to an 
eligible customer's account. Each time you navigate to their account, 
it checks whether they're eligible for a voucher and whether they're able 
to claim another today. If so, the voucher's value is credited to their 
account. Each time money is debited from their account, any remaining 
voucher balance is debited first before using their cash balance. 

Detailed documentation is in the "docs" directory.

## Quick start

1. Run `python3 manage.py migrate` to create the required models.

2. Run `python3 manage.py createsuperuser` to create a superuser. 

3. Start the development server by running `python3 manage.py runserver`
   and visit http://127.0.0.1:8000/admin/ to try out the system (you'll 
   need the Admin app enabled).

4. Visit http://127.0.0.1:8000/cashless/ to interact with the web sevice. 
   You'll need a NFC capable ID card and a USB card reader to enjoy all 
   the features on offer. 

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct. 

This app is written in python 3.6 using the django framework version 2.0.7.  

## Authors

* **PoignantWizard** - *Initial work* 

## License

This project is licensed under the 3-Clause BSD License - see the [LICENSE.md](LICENSE.md) file for details. 