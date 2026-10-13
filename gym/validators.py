import re
import math


def is_valid_username(username):
    
    if not isinstance(username, str):
        return False

    return bool(username.strip())


def is_valid_password(password):
    
    if not isinstance(password, str):
        return False

    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+$"
    return bool(re.fullmatch(pattern, password))


def is_valid_email(email):
    
    if not isinstance(email, str):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.fullmatch(pattern, email))


def is_positive_number(value):
    
    try:
        number = float(value)
        return math.isfinite(number) and number > 0
    except (TypeError, ValueError):
        return False


def is_positive_integer(value):
    
    try:
        number = int(value)
        return number > 0 and str(number) == str(value).strip().lstrip("+")
    except (TypeError, ValueError):
        return False