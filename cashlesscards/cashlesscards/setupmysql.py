import argparse
import MySQLdb


def mysql_setup(root_password, db, db_user, db_password):
    """Sets up the MySQL environment required by the cashless cards system"""
    server = MySQLdb.connect(
        host="localhost",
        user="root",
        password=root_password,
    )
    cursor = server.cursor()

    cursor.execute("CREATE DATABASE " + db + " CHARACTER SET UTF8;")

    create_user = "CREATE USER " + db_user + "@localhost IDENTIFIED BY '" \
                                                + db_password + "';"

    cursor.execute(create_user)
    cursor.execute("GRANT ALL PRIVILEGES ON " + db + ".* TO '" \
                                + db_user + "'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")


def main():
    """Entry point to program"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest="root", action="store", help="enter root password")
    parser.add_argument('-d', dest="db", action="store", help="enter the new database name")
    parser.add_argument('-u', dest="db_user", action="store", help="enter the new database user")
    parser.add_argument('-p', dest="db_password", action="store", \
                                    help="enter the new database user's password")
    args = parser.parse_args()

    mysql_setup(args.root, args.db, args.db_user, args.db_password)


if __name__ == '__main__':
    main()
