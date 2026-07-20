import psycopg

def connect_db():
   
    # Define db
    connection = psycopg.connect(
        'postgresql://neondb_owner:npg_lqKhEFAQW3e8@ep-soft-queen-awpsh3gb-pooler.c-12.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    )

    # Establish connection
    cursor = connection.cursor()

    return connection, cursor