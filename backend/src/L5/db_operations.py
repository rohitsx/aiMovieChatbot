from ..lib.db.psql import get_connection
import json

async def get_chat_history(username:str):
    db = await get_connection()

    if db:
        try:
            chat_history = await db.fetch("SELECT * FROM chat_history WHERE username = $1", username)
            json_output = [dict(record) for record in chat_history]

            print(json.dumps(json_output, indent=4, ensure_ascii=False))
        
            return json_output
        except Exception as e:
            print(f"Error executing SQL: {e}")
        finally:
            await db.close()
    else:
        print("Failed to connect to PostgreSQL.")

async def add_chat_history(username:str | None, human_msg:str, ai_msg):
    if not username:
        return
    db = await get_connection()

    if db:
        try:
            await db.execute("INSERT INTO chat_history (username, human_msg, ai_msg) VALUES ($1, $2, $3)", username, human_msg, ai_msg)
        except Exception as e:
            print(f"Error executing SQL: {e}")
        finally:
            await db.close()
    else:
        print("Failed to connect to PostgreSQL.")


async def check_username_exits(username:str):
    db = await get_connection()

    if db:
        try:
            result = await db.fetchval("SELECT COUNT(*) FROM chat_history WHERE username = $1", username)
            print(result)
            return result == 0
        except Exception as e:
            print(f"Error executing SQL: {e}")
        finally:
            await db.close()
    else:
        print("Failed to connect to PostgreSQL.")
