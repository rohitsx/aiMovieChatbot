from src.lib.db.psql import get_connection
from langchain_core.documents import Document
from src.lib.db.Qdrant import vector_store, client
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4
import asyncio
import concurrent.futures

async def process_record(record):
    script = record["script_text"].replace("  ", "").strip()
    if script:
        return Document(
            page_content=script,
            metadata={"movie_name": record["movie_name"].strip(), "script_url": record["script_url"].strip()}
        )
    return None

async def get_script():
    conn = await get_connection()
    if not conn:
        return "Failed to connect to PostgreSQL."
    try:
        cursor = await conn.fetch(
            "SELECT DISTINCT ON (script_text) script_text, movie_name, script_url FROM movie_scripts;"
        )
        tasks = [process_record(dict(i)) for i in cursor]
        documents = await asyncio.gather(*tasks)
        documents = [doc for doc in documents if doc is not None]  
        print(f"Fetched {len(documents)} non-empty scripts.")
        return documents
    except Exception as e:
        return ("data not found", e)

async def add_data_to_vector_store(documents):
    BATCH_SIZE = 1000  
    NUM_WORKERS = 10   
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            loop = asyncio.get_event_loop()

            async def process_batch(start_idx):
                end_idx = start_idx + BATCH_SIZE
                batch_docs = documents[start_idx:end_idx]
                batch_ids = [str(uuid4()) for _ in range(len(batch_docs))]
                await loop.run_in_executor(
                    executor,
                    lambda: vector_store.add_documents(documents=batch_docs, ids=batch_ids)
                )
                print(f"Processed batch {start_idx} to {end_idx}")

            tasks = [process_batch(i) for i in range(0, len(documents), BATCH_SIZE)]
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error adding data to vector store: {e}")

async def main():
    results = vector_store.similarity_search(query="Hii",k=1)
    if len(results) == 0:
        print("Populating vector store...")
        documents = await get_script()
        await add_data_to_vector_store(documents)
        print("Vector store population completed.")
    else:
        print( "Collection already exists, skipping data population.")




