import re


def clean_phone_number(number):
    return number.strip().replace(' ', '')


def clean_mx_with_regex(number):
    return re.sub(r'^\+521?', '', number)
