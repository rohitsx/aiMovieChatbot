from langchain_chroma import Chroma
from langchain_google_vertexai import VertexAIEmbeddings

embeddings = VertexAIEmbeddings(model="text-embedding-004")

vector_store = Chroma(
    collection_name="movie_scripts",
    embedding_function=embeddings,
)
