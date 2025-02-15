from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_google_vertexai import VertexAIEmbeddings

embeddings = VertexAIEmbeddings(model="text-embedding-004")

client = QdrantClient("http://localhost:6333")



vector_store = QdrantVectorStore(
    client=client,
    collection_name="movie_scripts",
    embedding=embeddings,
)
