import bcrypt
from flask import jsonify
from helpers.account_management.password_validation import password_is_valid

def delete(connection, cursor, email, password):

    # Locate user
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    # Check if user is not found
    if user is None:
        return False, "Email or password incorrect"

    stored_hash = user[2]
    if password_is_valid(password, stored_hash): 

        # Delete user
        query = "DELETE FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        connection.commit()
        return True, "Account deleted successfully"
    
    else:
        return False, "Email or password incorrect"