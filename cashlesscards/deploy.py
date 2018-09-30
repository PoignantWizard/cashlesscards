#!/usr/bin/env python3
import os
import getpass


SYSTEM_VERSION = 1.0


def get_packages():
    """Get required packages"""
    os.system("sudo apt-get update")
    packages = "sudo apt-get install " \
            + "python3-pip python3-dev python-mysqldb mysql-server libmysqlclient-dev "
    os.system(packages)


def python_packages():
    """Activate virtual environment and install required python packages"""
    cmd = "pip3 install -r requirements.txt"
    os.system(cmd)


def configure_mysql():
    """Set up MySQL database"""
    os.system("mysql_secure_installation")

    # get credentials
    root_password = getpass.getpass("Enter root password for MySQL: ")
    db = "cashlesscards"
    db_user = input("Enter new database username: ")
    db_password = getpass.getpass("Enter password: ")

    # sets up the MySQL environment required by the cashless cards system
    import MySQLdb
    server = MySQLdb.connect(
        host="localhost",
        user="root",
        password=root_password,
    )
    cursor = server.cursor()
    cursor.execute("CREATE DATABASE " + db + " CHARACTER SET UTF8;")
    create_user = "CREATE USER '" + db_user + "'@'localhost' IDENTIFIED BY '" \
                                                + db_password + "';"
    cursor.execute(create_user)
    cursor.execute("GRANT ALL PRIVILEGES ON " + db + ".* TO '" \
                                + db_user + "'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")

    # return details for use by other setup functions
    return db, db_user, db_password


def setup_credentials(db, db_user, db_password):
    """Set up credentials file"""
    from django.core.management import utils
    key = utils.get_random_secret_key()

    ssl = input("Has SSL been enabled on the server yet? (y/n) ")
    if ssl == "yes" or ssl == "Yes" or ssl == "y" or ssl == "Y":
        ssl = True
    else:
        ssl = False

    hosts = []
    i = 0
    print("Enter each allowed host. Leave the line blank", end=" ")
    print("and press enter to finish entering hosts.")
    while True:
        i += 1
        host = input("Enter host " + str(i) + ": ")
        if host:
            hosts.append(host)
        else:
            break

    contents = '"""\n' \
        + "Credentials required by in the cashless cards project\n" \
        + "Ensure this is not served and kept a secret!\n" \
        + '"""\n\n' \
        + "# CRSF token\n" \
        + "SECRET_KEY = '" + key + "'\n\n\n" \
        + "# MySQL database details\n" \
        + "DATABASE = '" + db + "'\n" \
        + "DB_USER = '" + db_user + "'\n" \
        + "DB_PASSWORD = '" + db_password + "'\n\n\n" \
        + "# allowed hosts\n" \
        + "ALLOWED_HOSTS = " + str(hosts) + "\n\n\n" \
        + "# site security\n" \
        + "SSL_ENABLED = " + str(ssl) + "\n"

    fname = "cashlesscards/credentials.py"
    with open(fname, 'w') as f:
        f.write(contents)


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
    """Migrate models, collect static files and create superuser"""
    # migrate models to database
    try:
        cmd = "python3 manage.py makemigrations"
        os.system(cmd)
        cmd = "python3 manage.py migrate"
        os.system(cmd)
    except:
        print("Error migrating models to database...")

    # collect static files
    try:
        cmd = "python3 manage.py collectstatic"
        os.system(cmd)
    except:
        print("Error collecting static files...")

    # create superuser
    try:
        cmd = "python3 manage.py createsuperuser"
        os.system(cmd)
    except:
        print("Error creating superuser...")


def launch_site():
    """Start the gunicorn webserver"""
    try:
        # set as executable
        cmd = "sudo chmod +x start.sh"
        os.system(cmd)
        # start webserver
        print("Launching webserver")
        cmd = "./start.sh &"
        os.system(cmd)
    except:
        print("Error starting webserver...")


def main():
    """Entry point to program"""
    get_packages()
    python_packages()
    db, db_user, db_password = configure_mysql()
    setup_credentials(db, db_user, db_password)
    deploy_production()
    setup_custom_settings()
    django_deploy()
    # conclusion
    print("Deployment complete!")
    launch_site()


if __name__ == '__main__':
    main()
