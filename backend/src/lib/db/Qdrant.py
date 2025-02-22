from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_google_vertexai import VertexAIEmbeddings
from qdrant_client.http.models import Distance, VectorParams
from src.lib.env import config    

embeddings = VertexAIEmbeddings(model="text-embedding-004")

if not config["QDRANT_URI"]:
    raise ValueError("QDRANT_URI is not set in .env")

client = QdrantClient(config["QDRANT_URI"])

def create_collection():
    try:
        client.create_collection(
            collection_name="movie_scripts",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print("Collection created successfully.")
    except Exception as e:
        print(f"Error creating collection: {e}")

create_collection()

vector_store = QdrantVectorStore(
    client=client,
    collection_name="movie_scripts",
    embedding=embeddings,
)


