import os
import ollama

EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]
