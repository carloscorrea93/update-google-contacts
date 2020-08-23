import re


def should_update_mx_phone_number(number):
    return bool(re.search(r'^\+521?\d{8,}$', number))
