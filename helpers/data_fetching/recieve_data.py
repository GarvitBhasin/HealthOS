from flask import request

def recieve_data():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    return email, password