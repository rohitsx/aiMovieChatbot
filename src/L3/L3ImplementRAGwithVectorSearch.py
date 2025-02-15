from ..lib.db.Qdrant import vector_store


def handler(request):
    script = request.json["script"]
    results = vector_store.similarity_search(query=script,k=1)
    for res in results:
        print(f"Retrieved Document: {res.page_content}")
        return {"movie_name": res.metadata["movie_name"], "script_url": res.metadata["script_url"], "script": res.page_content}
    return "data not found\n"

