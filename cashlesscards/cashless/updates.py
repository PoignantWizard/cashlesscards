import urllib.request
from . import customsettings


def check_current_version():
    """
    Compares local version to github to check
    whether the latest version is in use
    """
    url = "https://raw.githubusercontent.com/zakwarren/" \
        + "cashlesscards/master/cashlesscards/cashless/customsettings.py"
    content = urllib.request.urlopen(url)

    # find version in github file
    for line in content:
        line = line.decode('utf-8')
        if line[:7] == "VERSION":
            try:
                git_version = float(line[10:])
                current_version = customsettings.VERSION
            except:
                git_version = line[10:]
                current_version = str(customsettings.VERSION)

    # check git version against currently installed local version
    if git_version == current_version:
        version_match = True
    else:
        version_match = False
    return version_match, git_version
