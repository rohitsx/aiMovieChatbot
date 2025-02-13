from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    max_retries=6,
    stop=None,
)
