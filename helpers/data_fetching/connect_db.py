import psycopg
from dotenv import load_dotenv
import os
load_dotenv()

def connect_db():
   
    # Define db
    connection = psycopg.connect(
        host= os.getenv("DB_HOST"),
        dbname= os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        sslmode= os.getenv("SSL_MODE"),
        channel_binding= os.getenv("CHANNEL_BINDING"),
    )

    # Establish connection
    cursor = connection.cursor()

    return connection, cursor