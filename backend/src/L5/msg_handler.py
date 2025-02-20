from fastapi import WebSocket
from ..lib.db.Qdrant import vector_store
from ..lib.LLM import llm
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from ..L5.db_operations import add_chat_history
import time

set_llm_cache(SQLiteCache(database_path="src/cache/langchain.db"))

class msg_handler:
    async def main(self, ws, human_msg):
        if not human_msg:
            raise ValueError("Invalid message or userid")

        await self.send_response(human_msg, ws)

    async def get_script(self, human_msg):
        try:
            results = vector_store.similarity_search(query=human_msg,k=1)

            if not results:
                return  None, None, "data not found"
    
            res = results[0]
            return  res.metadata["movie_name"], res.metadata["script_url"], res.page_content

        except Exception:
            return  None, None,"data not found"

    async def send_response(self, human_msg:str, ws: WebSocket):
        try:
            start_time = time.time()

            movie_name, script_url, dialogue = await self.get_script(human_msg)

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

            ai_msg = llm.invoke(message)
            ai_res = ai_msg.content if ai_msg else "Can't reply to this message, try a different prompt"
            response = {"movie_name": movie_name, "script_url": script_url, "dialogue": dialogue, "ai_response": ai_res}


            print(f"CPU Response Time: {time.time() - start_time:.6f} seconds")

            print(ai_msg.content)
            await ws.send_json(response)
            return await add_chat_history(ws.query_params.get("username"), human_msg, ai_res)



        except Exception as err:
            print("Error:", err)
            raise


