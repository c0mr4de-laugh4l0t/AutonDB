import os
import ollama
from app.db.metadata import search_metadata

RESOLVER_MODEL = os.getenv("RESOLVER_MODEL", "phi3")

def resolve_query(query: str, caller_scope: list[str]) -> str | None:
    candidates = search_metadata(query, scope=caller_scope, top_k=5)
    if not candidates:
        return None

    candidate_text = "\n".join(
        f"ID: {c['id']} | Name: {c['name']} | Service: {c['service']} | Tags: {c['tags']}"
        for c in candidates
    )

    prompt = f"""You are a credential resolver. Given a user query and a list of credential records,
return ONLY the ID of the best matching record. If nothing matches, return NONE.
Do not explain. Do not return the key value. Return only the ID or NONE.

Query: {query}

Candidates:
{candidate_text}

Answer:"""

    response = ollama.chat(
        model=RESOLVER_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response["message"]["content"].strip()
    matched_ids = [c["id"] for c in candidates]
    return result if result in matched_ids else None
