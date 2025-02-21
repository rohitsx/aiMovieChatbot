from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_google_vertexai import VertexAIEmbeddings
from ..env import config    

embeddings = VertexAIEmbeddings(model="text-embedding-004")

if not config["QDRANT_URI"]:
    raise ValueError("QDRANT_URI is not set in .env")

client = QdrantClient(config["QDRANT_URI"])

vector_store = QdrantVectorStore(
    client=client,
    collection_name="movie_scripts",
    embedding=embeddings,
)
