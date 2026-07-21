import secrets, hashlib, smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta, UTC
from helpers.data_fetching.connect_db import *
from dotenv import load_dotenv
import os
load_dotenv()

def generate_and_save_token(user_email, connection, cursor):
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expiry = datetime.now() + timedelta(hours=1)
    
    query = "UPDATE users SET verification_token_hash = %s, token_expiry = %s WHERE email = %s"
    cursor.execute(query, (token_hash, expiry, user_email))
    connection.commit()

    return token


def send_verification_email(user_email, token):

    # Create email in memory
    msg = EmailMessage()
    msg["Subject"] = "Verify your HealthOS account"
    msg["From"] = "healthos.platform@gmail.com"
    msg["To"] = user_email
    verification_link = f"http://127.0.0.1:5000/verify?token={token}"

    msg.set_content(f"""
        Welcome to HealthOS!

        Verify your account here:
        {verification_link}
    """)

    msg.add_alternative(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 40px 20px;
                background: #fefef6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #222;
            }}

            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 18px;
                padding: 50px;
                box-shadow: 0 8px 25px rgba(0,0,0,.08);
                border: 1px solid #ececec;
                text-align: center;
            }}

            .logo {{
                width: 70px;
                margin-bottom: 15px;
            }}

            h1 {{
                margin: 0;
                font-size: 34px;
                font-weight: 700;
                color: #111;
            }}

            .tagline {{
                margin-top: 8px;
                color: #888;
                font-size: 15px;
            }}

            .divider {{
                width: 70px;
                height: 3px;
                background: black;
                margin: 35px auto;
                border-radius: 10px;
            }}

            p {{
                font-size: 17px;
                line-height: 1.7;
                color: #555;
                margin: 18px 0;
            }}

            .button {{
                display: inline-block;
                margin: 30px 0;
                padding: 15px 34px;
                background: black;
                color: white !important;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
            }}

            .button:hover {{
                background: #222;
            }}

            .expiry {{
                font-size: 14px;
                color: #888;
                margin-top: 25px;
            }}

            .footer {{
                margin-top: 45px;
                padding-top: 25px;
                border-top: 1px solid #ececec;
                font-size: 13px;
                color: #999;
                line-height: 1.6;
            }}

            .link {{
                color: black;
                word-break: break-all;
            }}
        </style>
        </head>

        <body>

        <div class="container">

            <img src="static/images/HealthOS-logo.png"
                alt="HealthOS Logo"
                class="logo">

            <h1>HealthOS</h1>

            <div class="tagline">
                Your operating system for lifelong health.
            </div>

            <div class="divider"></div>

            <p>
                Thank you for creating your HealthOS account.
            </p>

            <p>
                Before you can begin your assessment, please verify your email address. Please use the latest email that was sent to you.
            </p>

            <a class="button" href="{verification_link}">
                Verify Email
            </a>

            <p class="expiry">
                This verification link expires in <strong>1 hour</strong>.
            </p>

            <p class="expiry">
                If the button doesn't work, copy and paste this link into your browser:
            </p>

            <p class="link">
                {verification_link}
            </p>

            <div class="footer">
                If you didn't create a HealthOS account, you can safely ignore this email.
                <br><br>
                © HealthOS
            </div>

        </div>

        </body>
        </html>
    """, subtype="html")

    # Connect to smpt server
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls() # encrypt using TLS
    smtp.login(
        "healthos.platform@gmail.com",
        "psxt zyid bfqx ygms"
    )

    # Send email
    smtp.send_message(msg)
    smtp.quit()

def send_reset_email(user_email, token):

    # Create email in memory
    msg = EmailMessage()
    msg["Subject"] = "HealthOS account password reset"
    msg["From"] = "healthos.platform@gmail.com"
    msg["To"] = user_email
    verification_link = f"http://127.0.0.1:5000/reset-password?token={token}"

    msg.set_content(f"""
        Welcome to HealthOS!

        Verify your account here:
        {verification_link}
    """)

    msg.add_alternative(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 40px 20px;
                background: #fefef6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #222;
            }}

            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 18px;
                padding: 50px;
                box-shadow: 0 8px 25px rgba(0,0,0,.08);
                border: 1px solid #ececec;
                text-align: center;
            }}

            .logo {{
                width: 70px;
                margin-bottom: 15px;
            }}

            h1 {{
                margin: 0;
                font-size: 34px;
                font-weight: 700;
                color: #111;
            }}

            .tagline {{
                margin-top: 8px;
                color: #888;
                font-size: 15px;
            }}

            .divider {{
                width: 70px;
                height: 3px;
                background: black;
                margin: 35px auto;
                border-radius: 10px;
            }}

            p {{
                font-size: 17px;
                line-height: 1.7;
                color: #555;
                margin: 18px 0;
            }}

            .button {{
                display: inline-block;
                margin: 30px 0;
                padding: 15px 34px;
                background: black;
                color: white !important;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
            }}

            .button:hover {{
                background: #222;
            }}

            .expiry {{
                font-size: 14px;
                color: #888;
                margin-top: 25px;
            }}

            .footer {{
                margin-top: 45px;
                padding-top: 25px;
                border-top: 1px solid #ececec;
                font-size: 13px;
                color: #999;
                line-height: 1.6;
            }}

            .link {{
                color: black;
                word-break: break-all;
            }}
        </style>
        </head>

        <body>

        <div class="container">

            <img src="static/images/HealthOS-logo.png"
                alt="HealthOS Logo"
                class="logo">

            <h1>HealthOS</h1>

            <div class="tagline">
                Your operating system for lifelong health.
            </div>

            <div class="divider"></div>

            <p>
                Click the button below to reset your password. Please use the latest email that was sent to you.
            </p>

            <a class="button" href="{verification_link}">
                Verify Email
            </a>

            <p class="expiry">
                This verification link expires in <strong>1 hour</strong>.
            </p>

            <p class="expiry">
                If the button doesn't work, copy and paste this link into your browser:
            </p>

            <p class="link">
                {verification_link}
            </p>

            <div class="footer">
                If you didn't create a HealthOS account, you can safely ignore this email.
                <br><br>
                © HealthOS
            </div>

        </div>

        </body>
        </html>
    """, subtype="html")

    # Connect to smpt server
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls() # encrypt using TLS
    smtp.login(
        "healthos.platform@gmail.com",
        os.getenv("SMTP_PASSWORD")
    )

    # Send email
    smtp.send_message(msg)
    smtp.quit()