#!/usr/bin/env python3
import os
import getpass


SYSTEM_VERSION = 1.0


def get_packages():
    """Get required packages"""
    os.system("sudo apt-get update")
    packages = "sudo apt-get install " \
            + "python3-pip python3-dev mysql-server libmysqlclient-dev " \
            + "apache2 libapache2-mod-wsgi-py3"
    os.system(packages)


def virtual_environment():
    """Set up virtual environment"""
    os.system("sudo pip3 install virtualenv")
    os.system("virtualenv cashlesscardsenv")


def python_packages():
    """Activate virtual environment and install required python packages"""
    cmd = ". cashlesscardsenv/bin/activate && " \
        + "pip3 install -r requirements.txt"
    os.system(cmd)


def configure_mysql():
    """Set up MySQL database"""
    os.system("mysql_secure_installation")

    # get credentials
    root_password = getpass.getpass("Enter root password for MySQL: ")
    db = "cashlesscards"
    db_user = input("Enter new database username: ")
    db_password = getpass.getpass("Enter password: ")
    cmd = ". cashlesscardsenv/bin/activate && " \
        + "python3 cashlesscards/setupmysql.py -r " + root_password \
        + " -d " + db \
        + " -u " + db_user \
        + " -p " + db_password
    os.system(cmd)
    return db, db_user, db_password


def setup_credentials(db, db_user, db_password):
    """Set up credentials file"""
    cmd = ". cashlesscardsenv/bin/activate && " \
        + "python3 cashlesscards/setupcredentials.py -d " + db \
        + " -u " + db_user \
        + " -p " + db_password
    os.system(cmd)


def deploy_production():
    """Deploy production settings"""
    set_old_prod = "cashlesscards/settings_production.py"
    set_dev = "cashlesscards/settings_development.py"
    set_prod = "cashlesscards/settings.py"
    if os.path.isfile(set_prod) and os.path.isfile(set_old_prod):
        os.rename(set_prod, set_dev)
    if os.path.isfile(set_old_prod):
        os.rename(set_old_prod, set_prod)


def setup_custom_settings():
    """Setup custom settings"""
    lang = input("Enter your language code (e.g. en-gb): ")
    time = input("Enter your time zone (e.g. GB): ")
    currency = input("Enter your currency code (e.g. GBP): ")
    email = input("Enter the email address for sending password resets: ")

    contents = '"""\n' \
        + "Custom settings for cashless app in the cashless cards project\n" \
        + '"""\n\n' \
        + "# current version of the system\n" \
        + "VERSION = " + str(SYSTEM_VERSION) + "\n\n\n" \
        + "# language and timezone settings\n" \
        + "LANGUAGE_CODE = '" + lang + "'\n\n" \
        + "TIME_ZONE = '" + time + "'\n\n\n" \
        + "# default currency supplied to django-money module\n" \
        + "CURRENCY = '" + currency + "'\n\n\n" \
        + "# email for sending password reset tokens\n" \
        + "FROM_EMAIL = '" + email + "'\n\n\n" \
        + "# timing options for vouchers\n" \
        + "# delete rows to remove options from system\n" \
        + "# currently doesn't support custom timings\n" \
        + "TIMING = (\n" \
        + '    ("daily", "Daily"),\n' \
        + '    ("weekly", "Weekly"),\n' \
        + '    ("monthly", "Monthly"),\n' \
        + '    ("yearly", "Yearly"),\n' \
        + ")\n"

    fname = "cashless/customsettings.py"
    with open(fname, 'w') as f:
        f.write(contents)


def django_deploy():
    """Migrate models and create superuser"""
    # migrate models to database
    try:
        cmd = ". cashlesscardsenv/bin/activate && " \
            + "python3 manage.py makemigrations"
        os.system(cmd)
        cmd = ". cashlesscardsenv/bin/activate && " \
            + "python3 manage.py migrate"
        os.system(cmd)
    except:
        print("Error migrating models to database...")


    # create superuser
    try:
        cmd = ". cashlesscardsenv/bin/activate && " \
            + "python3 manage.py createsuperuser"
        os.system(cmd)
    except:
        print("Error creating superuser...")


def configure_apache():
    """Configure apache web server"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    content = "<VirtualHost *:80>\n\n" \
            + "    Alias /static " + dir_path + "/cashless/static\n" \
            + "    <Directory " + dir_path + "/cashless/static>\n" \
            + "        Require all granted\n" \
            + "    </Directory>\n\n" \
            + "    <Directory " + dir_path + "/cashlesscards>\n" \
            + "        <Files wsgi.py>\n" \
            + "            Require all granted\n" \
            + "        </Files>\n" \
            + "    </Directory>\n\n" \
            + "    WSGIDaemonProcess cashlesscards " \
            + "python-home=" + dir_path + "/cashlesscardsenv " \
            + "python-path=" + dir_path + "\n" \
            + "    WSGIProcessGroup cashlesscards\n" \
            + "    WSGIScriptAlias / " + dir_path + "/cashlesscards/wsgi.py\n\n" \
            + "    ErrorLog /var/log/apache2/cashless-error.log\n" \
            + "    LogLevel warn\n" \
            + "    CustomLog /var/log/apache2/cashless-access.log combined\n\n" \
            + "</VirtualHost>"
    fname = "000-default.conf"
    fdest = "/etc/apache2/sites-available/000-default.conf"
    with open(fname, 'w') as f:
        f.write(content)
    os.system("sudo mv " + fname + " " + fdest)
    # configure firewall and check and apply apache config
    os.system("sudo ufw allow 'Apache Full'")
    os.system("sudo apache2ctl configtest")
    os.system("sudo systemctl restart apache2")


def main():
    """Entry point to program"""
    get_packages()
    virtual_environment()
    python_packages()
    db, db_user, db_password = configure_mysql()
    setup_credentials(db, db_user, db_password)
    deploy_production()
    setup_custom_settings()
    django_deploy()
    configure_apache()
    # conclusion
    print("Deployment complete!")


if __name__ == '__main__':
    main()
