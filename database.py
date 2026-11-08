import psycopg

def get_connection():

    conn = psycopg.connect(
        dbname="library_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    return conn