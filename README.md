# Cashless card system

A system designed to provide a cashless service in a "closed" environment, 
such as offices, clinics, and schools. 

Detailed documentation is in the "docs" directory.

## Quick start

1. Run `python manage.py migrate` to create the required models.

2. Start the development server and visit http://127.0.0.1:8000/admin/
   to try out the system (you'll need the Admin app enabled).

3. Visit http://127.0.0.1:8000/cashless/ to interact with the web sevice. 
   You'll need a NFC capable ID card to enjoy all the features on offer. 

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct. 

This app is written in python 3.6 using the django framework version 2.0.7.  

## Authors

* **PoignantWizard** - *Initial work* 

## License

This project is licensed under the 3-Clause BSD License - see the [LICENSE.md](LICENSE.md) file for details. 