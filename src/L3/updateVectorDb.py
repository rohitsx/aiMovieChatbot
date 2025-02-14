from ..lib.db.psql import get_connection   
from langchain_core.documents import Document
from ..lib.db.chromadb import vector_store
from uuid import uuid4
import time
import asyncio

async def get_script():
    conn = await get_connection()
    if not conn:
        return "Failed to connect to PostgreSQL."
    try:
        cursor = await conn.fetch(
            "SELECT DISTINCT ON (script_text) script_text, movie_name FROM movie_scripts;"
        )
        documents = []
        for i in cursor:
            record = dict(i) 
            script = record["script_text"].replace("  ", "").strip() 
            if script:  
                documents.append(Document(
                    page_content=script, metadata={"movie_name": record["movie_name"].strip()}
                ))

        print(f"Fetched {len(documents)} non-empty scripts.")  
        return documents
    except Exception as e:
        return ("data not found", e)

async def add_data_to_vector_store(documents):
    start_time = time.perf_counter()
    BATCH_SIZE = 500
    tasks = []
    for i in range(0, len(documents), BATCH_SIZE):
        print(f"Adding batch {i} to chromadb")
        batch_docs = documents[i:i + BATCH_SIZE]
        batch_ids = [str(uuid4()) for _ in range(len(batch_docs))]

        tasks.append(vector_store.aadd_documents(documents=batch_docs, ids=batch_ids))

    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error adding data to vector store: {e}")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time  
    print(f"Total execution time: {elapsed_time:.2f} seconds")

async def main():
    try:
        results = vector_store.get()
        has_data = len(results['ids']) > 0
        if has_data:
            return
    except Exception as e:
        return f"Error checking chromadb: {e}"

    documents = await get_script()
    if isinstance(documents, str):  # Check if an error message was returned
        print(documents)
        return

    await add_data_to_vector_store(documents)
    if vector_store:
        print("Vector store created successfully.")
    else:
        print("Failed to create vector store.")

# Run the main function
asyncio.run(main())
