import chromadb
from app.core.embedder import embed

client = chromadb.PersistentClient(path="chroma_data")
collection = client.get_or_create_collection("credentials")

def store_metadata(record_id: str, name: str, service: str, tags: list[str], owner: str):
    text = f"{name} {service} {' '.join(tags)}"
    vector = embed(text)
    collection.add(
        ids=[record_id],
        embeddings=[vector],
        metadatas=[{"name": name, "service": service, "tags": ",".join(tags), "owner": owner}]
    )

def search_metadata(query: str, scope: list[str], top_k: int = 5) -> list[dict]:
    vector = embed(query)
    results = collection.query(
        query_embeddings=[vector],
        n_results=top_k,
        where={"owner": {"$in": scope}} if scope else None
    )
    if not results["ids"][0]:
        return []
    return [
        {
            "id": results["ids"][0][i],
            "name": results["metadatas"][0][i]["name"],
            "service": results["metadatas"][0][i]["service"],
            "tags": results["metadatas"][0][i]["tags"],
        }
        for i in range(len(results["ids"][0]))
    ]

def delete_metadata(record_id: str):
    collection.delete(ids=[record_id])
