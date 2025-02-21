import asyncpg
from ..env import config

async def get_connection():
    try:
        conn = await asyncpg.connect(config["PSQL_URI"])
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
            print("movie_scripts Table created successfully.")
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
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    human_msg TEXT NOT NULL,
                    ai_msg TEXT 
                )
            """)
            print("chat_history Table created successfully.")
        except Exception as e:
            print(f"Error executing SQL: {e}")
        finally:
            await conn.close()
    else:
        print("Failed to connect to PostgreSQL.")
