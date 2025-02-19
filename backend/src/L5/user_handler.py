from fastapi import WebSocket, WebSocketDisconnect
from ..lib.db.psql import create_chat_history_table, get_connection
from ..lib.LLM import llm
import time


async def create_userid(username:str):
    def create_chat_history_table()
    db = await get_connection()

    if db:
        try: 
            await db.execute("""
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
            await db.close()
    else:
        print("Failed to connect to PostgreSQL.")

async def get_chat_history(userid):
    print(userid)
