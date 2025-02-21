from src.lib.LLM import llm


async def handler(request):
    req_json = await request.json()
    if "character" in req_json and "user_message" in req_json:
        return generate_character_res(req_json)
    else:
        return "invalid request\n"

def generate_character_res(req_json):
   
    message = [
        (
            "system",
            f"You are a movie character, and your personality is based on {req_json['character']}. Whenever you respond, your tone, language, and style should reflect this character’s unique way of speaking. Always stay true to the character's personality, mannerisms, and worldview, even if the conversation is about something outside the movie."
        ),
        ("human", req_json["user_message"]),
    ]

    ai_msg = llm.invoke(message)

    return {
        "character": req_json["character"],
        "user_message": req_json["user_message"],
        "ai_response": ai_msg.content,
    }

