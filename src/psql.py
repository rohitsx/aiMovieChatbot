import psycopg2
def get_connection():
    try:
        conn = psycopg2.connect(
            database="mydatabase",
            user="myuser",
            password="mypassword",
            host="127.0.0.1",
            port=5432,
        )
        return conn.cursor()
    except:
        return False

psqlClient = get_connection()
if psqlClient:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")
