import argparse
from django.core.management import utils

def setup_credentials(db, db_user, db_password):
    """Set up credentials file"""
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


def main():
    """Entry point to program"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest="db", action="store", help="enter the new database name")
    parser.add_argument('-u', dest="db_user", action="store", help="enter the new database user")
    parser.add_argument('-p', dest="db_password", action="store", \
                                    help="enter the new database user's password")
    args = parser.parse_args()

    setup_credentials(args.db, args.db_user, args.db_password)


if __name__ == '__main__':
    main()
