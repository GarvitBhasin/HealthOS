import bcrypt

def password_is_valid(password, stored_hash):
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True
    else:
        return False