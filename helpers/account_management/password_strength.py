def password_is_strong(password) :
    password_validity = (
        len(password) > 8
        and any(char.isdigit() for char in password)
        and any(char.isalpha() for char in password)
        and any(
            not char.isalnum() for char in password
        )
    )
    return password_validity