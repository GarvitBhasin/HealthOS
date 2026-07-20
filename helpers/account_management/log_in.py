from flask import jsonify
import bcrypt, re
from helpers.account_management.email_validity import *
from helpers.account_management.password_strength import *
from helpers.account_management.password_validation import password_is_valid

def log_in(cursor, email, password):

    if not email_is_valid(email):
        return False, "Please enter a valid email", None
    if not password_is_strong(password): 
        return False, "Email or password incorrect", None

    # Find email
    query = "SELECT * FROM users WHERE email = %s;"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    # Check if email is not found
    if user is None:
        return False, "Email not registered", None
    
    # Verify password hashes
    else:
        stored_hash = user[2]
        user_id = user[0]
        if password_is_valid(password, stored_hash): 
            return True, "Logged in successfully.", user_id
        else:
            return False, "Email or password incorrect.", None