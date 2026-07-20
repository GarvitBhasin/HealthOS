from helpers.account_management.email_validity import *
from helpers.account_management.password_strength import *
from helpers.account_management.email_verification import *
import bcrypt

def sign_up(connection, cursor, email, password, creationDate):

    # Check email and password validity
    if not email_is_valid(email):
        return False, "Please enter a valid email"
    if not password_is_strong(password): 
        return False, "Password must be atleast 8 characters long, have atleast one digit, one symbol and one letter."

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Register user
    query = "INSERT INTO users (email, password_hash, creation_date) VALUES (%s, %s, %s);"
    cursor.execute(query, (email, hashed_password, creationDate))
    connection.commit()

    # Email verificaion
    token = generate_and_save_token(email, connection, cursor)
    send_verification_email(email, token)

    # Extract new user's id
    query = "SELECT * FROM users WHERE email = %s;"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    user_id = user[0]

    # Close connection
    cursor.close()
    connection.close()

    return True, user_id