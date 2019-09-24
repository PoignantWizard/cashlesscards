#!/usr/bin/env python3
import os


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

def main():
    """Entry point to program"""
    get_packages()
    python_packages()


if __name__ == '__main__':
    main()
