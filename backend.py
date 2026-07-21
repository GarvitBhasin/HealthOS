from flask import Flask, render_template, jsonify, request, redirect
from flask import session
from dotenv import load_dotenv
from datetime import timedelta, datetime
import os
import json
from helpers.data_fetching.connect_db import *
from helpers.data_fetching.recieve_data import *
from helpers.data_fetching.find_assessment import *
from helpers.account_management.sign_up import *
from helpers.account_management.log_in import *
from helpers.account_management.delete import *
from helpers.account_management.email_verification import *
from helpers.assessment_logic.assessment import *
from helpers.assessment_logic.algorithm import *
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=4)
 
# --- ACCOUNT MANAGEMENT --- #

# SIGN UP 
@app.route("/api/sign-up", methods=["POST"])
def signup_api():

    # Recieve user data
    email, password = recieve_data()
    creationDate = request.json.get("creationDate")

    try:
        # Connect to db
        connection, cursor = connect_db()

        # Create user in db and create user's session
        success, result = sign_up(connection, cursor, email, password, creationDate)

        if not success:
            return jsonify({
                "message": result
            }), 422

        session["user_id"] = result

        return jsonify({
            "message": "Account successfully created."
        }), 201
    
    # Check if email already exists
    except psycopg.IntegrityError:
        return jsonify({"message": "An account with this email already exists."}), 409
    
    # Check for db connection fail
    except psycopg.Error as err: 
        print(f"Error: {err}")
        return jsonify({"message": "Database transaction failed."}), 500

# EMAIL VERIFICATION  
@app.route("/api/email-sent", methods=["POST"])
def email_sent():
    try:
        connection, cursor = connect_db()

        # Find email from the user_id stored in cookies
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session["user_id"],))
        user = cursor.fetchone()
        user_email = user[1]
        is_verified = user[4]

        if is_verified:
            return jsonify({"message": "Account is already verified."}), 400
        
        # Generate, save and send token via email
        token = generate_and_save_token(user_email, connection, cursor)
        send_verification_email(user_email, token)

        cursor.close()
        connection.close()

        return jsonify({"message": "Verification email sent successfully."}), 200
    
    except Exception as err:
        print(err)
        return jsonify({"message": "Unable to send verification email."}), 500

    except psycopg.Error as err: 
        print(err)
        return jsonify({"message": "Database transaction failed."}), 500
    
@app.route("/api/verify", methods=["POST"])
def verify():
    token = request.args.get("token")

    try:
        connection, cursor = connect_db()

        # Check if token matches
        received_hash = hashlib.sha256(token.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE verification_token_hash = %s", (received_hash,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({
                "message": "Could not find verification token."
            }), 404

        id = user[0]
        expiry = user[6]

        # Check if token expired
        if datetime.now(UTC) > expiry:
            return jsonify({
                "message": "Verification token is expired."
            }), 400
        
        # Set verification status as true and clear token
        cursor.execute("UPDATE users SET is_verified = TRUE, verification_token_hash = NULL, token_expiry = NULL WHERE user_id = %s ", (id,))
        connection.commit()

        return jsonify({
            "message": "Account verified successfully."
        }), 200
    
    except psycopg.Error as err: 
        print(err)
        return jsonify({"message": "Database transaction failed."}), 500

    finally:
        cursor.close()
        connection.close()

# LOGIN
@app.route("/api/login", methods=["POST"])
def login_api():

    # Recieve user data
    email, password = recieve_data()
    rememberMe = request.json.get("rememberMe")

    try:

        # Connect to db
        connection, cursor = connect_db()

        success, message, user_id = log_in(cursor, email, password)

        # Check if login was successful
        if success:
            session["user_id"] = user_id
            session.permanent = rememberMe

            return jsonify({
                "message": message,
            }), 200
        else:
            return jsonify({
                "message": message,
            }), 401

    # Check for db connection fail
    except psycopg.Error as err: 
        print(f"Error: {err}")
        return jsonify({"message": "Database transaction failed."}), 500
    
    finally:
        cursor.close()
        connection.close()

@app.route("/api/logout", methods=["POST"])
def log_out():

    # Remove user from session
    session.clear()

    return jsonify({
        "message": "Successfully logged out."
    })

# DELETE
@app.route("/api/delete", methods=["POST"]) 
def delete_api():

    # Recieve user data
    email, password = recieve_data()

    try:

        # Connect to db and remove user
        connection, cursor = connect_db()
        success, message = delete(connection, cursor, email, password)
        
        if success:
            # Clear user data in cookies
            session.clear()

            return jsonify({
                "message": message
            }), 200
        else: 
            return jsonify({
                "message": message
            }), 401

    # Check for db connection fail   
    except psycopg.Error as err: 
        print(f"Error: {err}")
        return jsonify({"message": "Database transaction failed."}), 500
    
    finally:
        cursor.close()
        connection.close()

# PASSWORD RESET
@app.route("/api/reset-email-sent", methods=["POST"])
def email_sent_reset():
    email = request.json.get("email")

    if not email_is_valid(email):
        return jsonify({
            "message": "Please enter a valid email."
        }), 422

    try:
        connection, cursor = connect_db()

        # Find email from the user_id stored in cookies
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({
                "message": "Email not registered."
            }), 401
        
        # Generate, save and send token via email
        token = generate_and_save_token(email, connection, cursor)
        send_reset_email(email, token)

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Password reset email sent successfully.", 
        }), 200
    
    except Exception as err:
        print(err)
        return jsonify({"message": "Unable to send password reset email."}), 500

    except psycopg.Error as err: 
        print(err)
        return jsonify({"message": "Database transaction failed."}), 500
    
@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    token = request.json.get("token")
    data = request.json
    password = data.get("pass")
    confirmPassword = data.get("confirmPass")

    try:
        connection, cursor = connect_db()

        # Check if token matches
        received_hash = hashlib.sha256(token.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE verification_token_hash = %s", (received_hash,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({
                "message": "Could not find verification token."
            }), 404

        # Check if token expired
        expiry = user[6]
        if datetime.now(UTC) > expiry:
            return jsonify({
                "message": "Verification token is expired."
            }), 400
        
        # Check if password combination matches
        if password != confirmPassword:
            return jsonify({
                "message": "Password pairs do not match."
            }), 422
        
        if not password_is_strong(password):
            return jsonify({
                "message": "Password must be atleast 8 characters long, have atleast one digit, one symbol and one letter."
            }), 422
        
        id = user[0]

        # Change password and clear tokens
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("UPDATE users SET password_hash = %s, verification_token_hash = NULL, token_expiry = NULL WHERE user_id = %s", (hashed_password, id))
        connection.commit()

        return jsonify({
            "message": "Password reset successfully."
        }), 200
    
    except psycopg.Error as err: 
        print(err)
        return jsonify({"message": "Database transaction failed."}), 500

    finally:
        cursor.close()
        connection.close()

# Used by frontend to access user data
@app.route("/api/me")
def me():
    if "user_id" in session:

        try:
            # Connect to db
            connection, cursor = connect_db()

            # Find user from the user_id stored in cookies
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (session["user_id"],))
            user = cursor.fetchone()
            user_email = user[1]
            creation_date = user[3]
            is_verified = user[4]

            cursor.close()
            connection.close()

            return jsonify({
                "authenticated": True,
                "user_email": user_email,
                "creation_date": str(creation_date),
                "is_verified": is_verified
            })
        
        except psycopg.Error as err: 
            print(f"Error: {err}")
            return jsonify({"message": "Database transaction failed."}), 500
    
    return jsonify({
        "authenticated": False
    })

# --- ASSESSMENT LOGIC --- #

@app.route("/api/submit", methods=["POST"])
def recieve_results():

    # Save answers in cookie and get user_id
    responses = request.json
    if responses is None:
        return jsonify({
            "message": "No assessment found"}
        ), 400
    
    user_id = session.get("user_id")

    print(responses)
    
    try:
        connection, cursor = connect_db()

        results = calculate(responses)
        results_json = json.dumps(results)

        # Add user's result to db
        query = "INSERT INTO assessments (user_id, results_json) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET results_json = EXCLUDED.results_json"
        cursor.execute(query, (user_id, results_json))
        connection.commit()

        return jsonify({
            "message": "Responses successfully recieved."
        })
    
    except psycopg.Error as err: 
        print(f"Error: {err}")
        return jsonify({"message": "Database transaction failed."}), 500
    
    finally:    
        cursor.close()
        connection.close()

@app.route("/api/results")
def calculate_results():
    if "user_id" in session:

        user_id = session.get("user_id")

        try:
            connection, cursor = connect_db()
            
            row = find_assessment(cursor, user_id)

            if row is None:
                return jsonify({
                    "message": "No assesssments found"
                }), 404

            return jsonify({
                "message": "Assessment found",
                "assessment": row[2]
            }), 200
        
        except psycopg.Error as err: 
            print(f"Error: {err}")
            return jsonify({"message": "Database transaction failed."}), 500
        finally:
            cursor.close()
            connection.close()
        
    return redirect("/login")

# --- RENDERING PAGES --- #

# UNPROTECTED

@app.route("/")
def home():
    return render_template("public/index.html")

@app.route("/assessment")
def assessment_page():
    return render_template("public/assessment.html")

@app.route("/faq")
def faq():
    return render_template("public/faq.html")

@app.route("/sign-up")
def signup_page():
    if "user_id" in session:
        return redirect("/")

    return render_template("auth/sign-up.html")

@app.route("/login")
def login_page():
    if "user_id" in session:
        return redirect("/")

    return render_template("auth/login.html")

@app.route("/reset-password")
def password_reset_page():
    return render_template("auth/pwreset.html")

@app.route("/reset-email-sent")
def reset_email_page():
    return render_template("auth/pwreset-email.html")

# PROTECTED

@app.route("/user-settings")
def settings():
    if "user_id" in session:
        return render_template("account/user-settings.html")
    
    return redirect("/login")

@app.route("/email-sent")
def email_sent_page():
    if "user_id" in session:
        return render_template("auth/email-sent.html")
    
    return redirect("/login")

@app.route("/verify")
def verify_page():
    if "user_id" in session:
        return render_template("auth/verify.html")
    
    return redirect("/login")

@app.route("/assessment-questions")
def assessment_questions():
    if "user_id" in session:

        user_id = session["user_id"]
        retake = request.args.get("retake")

        try:
            connection, cursor = connect_db()

            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            is_verified = user[4]

            if not is_verified:
                return redirect("/email-sent")

            row = find_assessment(cursor, user_id)

            if row is not None and retake != "true":
                return redirect("/results")
            
            return render_template("app/assessment-questions.html")
        
        except psycopg.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    
    return redirect("/login")

@app.route("/api/assessment-questions")
def load_assessment():
    return jsonify(assessment)

@app.route("/results")
def results():
    if "user_id" in session:

        user_id = session["user_id"]

        try:
            connection, cursor = connect_db()

            row = find_assessment(cursor, user_id)

            if row is None:
                return redirect("/assessment-questions")

            return render_template("app/results.html")
        
        except psycopg.Error as err:
            print(f"Error: {err}")
            return redirect("/")
        finally:
            cursor.close()
            connection.close()
    
    return redirect("/login")

@app.route("/dashboard")
def dashboard_page():
    if "user_id" in session:
        return render_template("app/dashboard.html")
    
    return redirect("/login")
# ERROR PAGES

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("errors/405.html"), 405

@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500

if __name__ == "__main__":
    app.run()