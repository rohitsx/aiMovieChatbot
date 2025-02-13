from ..lib.psql import get_connection 
from ..lib.LLM import llm

async def handler(request):
    req_json = request.json
    if "script" in req_json:
        return await find_script(req_json)
    return "invalid request\n"

async def find_script(req_json):
    conn = await get_connection()
    if not conn:
        return "Failed to connect to PostgreSQL."

    try:
        script = req_json["script"]
        cursor = await conn.fetch(
            f"""SELECT * FROM movie_scripts 
            WHERE similarity(script_text, '{script}') > 0.8
            ORDER BY similarity(script_text, '{script}') DESC
            LIMIT 1;"""
        )
        script_text = dict(cursor[0]) 
        return script_text
        
    except Exception:
        return send_ai_response(req_json["script"])
    finally:
        await conn.close()


def send_ai_response(script):
    message = [
        (
            "system",
            """When a user provides a dialogue from a movie script that is not found in the database, respond with:
            'Dialogue not found.'

            Then, generate an interesting fact related to the movie, its actors, the production process, or any behind-the-scenes detail that adds value to the user's query. Keep the fact concise, engaging, and relevant to the movie if possible"""
        ),
        ("human", script),
    ]

    ai_msg = llm.invoke(message)
    return {"ai_response": ai_msg.content}

