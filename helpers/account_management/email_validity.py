import re

def email_is_valid(email) :
    email_validity = bool(re.match(r"^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$", email))
    return email_validity