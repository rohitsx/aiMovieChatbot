from src.lib.db.Qdrant import vector_store
from src.lib.LLM import llm
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
import time


set_llm_cache(SQLiteCache(database_path="src/cache/langchain.db"))

async def handler(req):
    start_time = time.time()

    human_msg, movie_name, script_url, dialogue = await get_script(req)
    message = [
        (
            "system",
            f"""
            you are an AI assistant that specializes in understanding and generating responses based on movie scripts and dialogues. You have been provided with relevant data retrieved through a similarity search from a vector database. The data includes:

            Movie Name: {movie_name}
            Script URL: {script_url}
            Main Dialogue: {dialogue}
            Using this information, generate a response that share some facts around it. If the dialogue is a question, provide a natural response. and if the dialogue not found mention no dialogue found of the match.
           """
        ),
        ("human", human_msg),
    ]

    try:
        ai_msg = llm.invoke(message)
        ai_response = ai_msg.content
    except Exception:
        ai_response = "No data on vector db, If you are a developer please check the Qdrant DB"

    response = {"movie_name": movie_name, "script_url": script_url, "dialogue": dialogue, "ai_response": ai_response}

    print(f"CPU Response Time: {time.time() - start_time:.6f} seconds")
    return response


async def get_script(request):
    try:
        script = await request.json()
        human_msg = script["script"]

        if not human_msg:
            raise ValueError("Script not found.")

        
        results = vector_store.similarity_search(query=human_msg,k=1)

        if not results:
            return None, None, None, "data not found"
    
        res = results[0]
        return human_msg, res.metadata["movie_name"], res.metadata["script_url"], res.page_content

    except Exception:
        return None, None, None,"data not found"



