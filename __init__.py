from datetime import datetime
import re

ONE_MB = 2**20
INT_SIZE = 2 ** 63 # 63 bits plus 1 bit for sign = 64 bit signed integer
EMAIL_USER = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
EMAIL_DOMAIN = re.compile(r'''
    ^(?:[a-z0-9][a-z0-9\-]{0,62}\.)+ # subdomain
    [a-z]{2,}$                       # TLD
''', re.I | re.VERBOSE)

# based on Django's but with limited schemes: https://github.com/django/django/blob/master/django/core/validators.py
URL = re.compile(
    r'^(?:http|https)://' # scheme
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|' # domain
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$',
re.IGNORECASE)


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


def validateRequiredText(source, max_length=ONE_MB, newlines=True):

    return validateRequiredString(source, max_length=max_length, newlines=newlines)


def validateEmail(source):

    valid, value = validateString(source)

    if valid and value:
        parts = value.split('@')
        if len(parts) != 2:
            valid = False
        else:
            username, domain = parts

            if not EMAIL_USER.search(username) or not EMAIL_DOMAIN.search(domain):
                valid = False

    return valid, value


def validateRequiredEmail(source):

    valid, value = validateEmail(source)

    if valid and not value:
        valid = False

    return valid, value


def validatePhone(source):

    valid, value = validateString(source)

    if valid and value:
        digits = [char for char in value if char.isdigit()]
        length = len(digits)
        if length < 10 or length > 15:
            valid = False
        else:
            if length == 10:
                # assume US/Canada with the country code missing
                digits = ['1'] + digits
            value = '+' + ''.join(digits)

    return valid, value


def validateRequiredPhone(source):

    valid, value = validatePhone(source)

    if valid and not value:
        valid = False

    return valid, value


def validateUrl(source):

    valid, value = validateString(source)

    if valid and value:
        if '//' not in value:
            value = 'http://' + value

        if not URL.search(value):
            valid = False

    return valid, value


def validateRequiredUrl(source):

    valid, value = validateUrl(source)

    if valid and not value:
        valid = False

    return valid, value


def validateChoices(source, choices):

    valid, value = validateString(source)

    if valid:
        valid = value in choices

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


def validateFloat(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1):

    valid = True
    try:
        value = float(source)
    except:
        value = 0.0
        valid = False

    if valid and (min_amount > value or max_amount < value):
        valid = False

    return valid, value


def validateDateTime(source, date_format="%Y-%m-%dT%H:%M", future_only=False, past_only=False):
    # note that this is not aware of timezones
    # recommend ISO format for sending from JS or other non-user sources: "%Y-%m-%dT%H:%M:%S.%fZ"
    assert not future_only or not past_only, "There are no dates in both the future and the past."

    valid = True
    try:
        value = datetime.strptime(source, date_format)
    except:
        value = None
        valid = False

    if valid:
        if future_only and value < datetime.utcnow():
            valid = False
        elif past_only and value > datetime.utcnow():
            valid = False

    return valid, value


def validateDate(source, date_format="%Y-%m-%d", future_only=False, past_only=False):

    valid, value = validateDateTime(source, date_format=date_format, future_only=future_only, past_only=past_only)

    if value:
        value = value.date()

    return valid, value


def validateTime(source, time_format="%H:%M"):

    valid, value = validateDateTime(source, date_format=time_format)
    
    if value:
        value = value.time()

    return valid, value
