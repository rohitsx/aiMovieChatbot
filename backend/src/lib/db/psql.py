import asyncpg

async def get_connection():
    try:
        conn = await asyncpg.connect(
            database="mydatabase",
            user="myuser",
            password="mypassword",
            host="127.0.0.1",
            port=5432,
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


async def create_table():
    conn = await get_connection()
    if conn:
        try:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS movie_scripts (
                    id SERIAL PRIMARY KEY,
                    movie_name TEXT NOT NULL,
                    script_url TEXT NOT NULL,
                    script_text TEXT
                );

                CREATE EXTENSION IF NOT EXISTS pg_trgm;
                """
            )
            print("Table created successfully.")
        except Exception as e:
            print(f"Error executing SQL: {e}")
        finally:
            await conn.close()
    else:
        print("Failed to connect to PostgreSQL.")


async def create_chat_history_table():
    conn = await get_connection();

    if conn:
        try: 
            await conn.execute("""
                CREATE TABLE ID NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)
            print("chat_history Table created successfully.")
        except Exception as e:
            print(f"Error executing SQL: {e}")
        finally:
            await conn.close()
    else:
        print("Failed to connect to PostgreSQL.")
