from ..lib.db.chromadb import vector_store


def handler(request):
    script = request.json["script"]
    print(script)
    results = vector_store.similarity_search(query=script,k=1)
    for res in results:
        print(f"Retrieved Document: {res.page_content}")
    return "working\n"

