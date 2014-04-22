
from datetime import datetime
import re

ONE_MB = 2**20
INT_SIZE = 2 ** 63 # 63 bits plus 1 bit for sign = 64 bit signed integer
EMAIL_USER = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
EMAIL_DOMAIN = re.compile(r'''
    ^(?:[a-z0-9][a-z0-9\-]{0,62}\.)+ # subdomain
    [a-z]{2,}$                       # TLD
''', re.I | re.VERBOSE)


def validateString(source, max_length=500, newlines=False):

    valid = True
    try:
        value = unicode(source) # defaults to utf-8 automatically
    except:
        value = ''
        valid = False

    if valid:
        value = value.strip()

        if len(value) > max_length:
            valid = False
        elif not newlines and ('\n' in value or '\r' in value):
            valid = False

    return valid, value


def validateRequiredString(source, max_length=500, newlines=False):

    valid, value = validateString(source, max_length=max_length, newlines=newlines)

    if valid and not value:
        valid = False

    return valid, value


def validateText(source, max_length=ONE_MB, newlines=True):

    return validateString(source, max_length=max_length, newlines=newlines)


def validateEmail(source):

    valid, value = validateRequiredString(source)

    if valid:
        parts = value.split('@')
        if len(parts) != 2:
            valid = False
        else:
            username, domain = parts

            if not EMAIL_USER.search(username) or not EMAIL_DOMAIN.search(domain):
                valid = False

    return valid, value


def validateBool(source):

    valid = True
    # this can't throw an exception as all types have a boolean value, so no need to wrap it in a try
    value = bool(source)

    return valid, value


def validateInt(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1):
    # one is subtracted from the max amount because 0 counts as a possible value on the positive side

    valid = True
    try:
        value = int(source)
    except:
        value = 0
        valid = False

    if valid and (min_amount > value or max_amount < value):
        valid = False

    return valid, value


def validateDate(source, date_format="%m/%d/%Y", keep_time=False, future_only=True):

    valid = True
    try:
        value = datetime.strptime(source, date_format)
    except:
        value = None
        valid = False

    if valid:
        if not keep_time:
            # remove time to make this represent midnight
            value = value.replace(hour=0, minute=0, second=0, microsecond=0)
        if future_only and value > datetime.utcnow():
            valid = False

    return valid, value
