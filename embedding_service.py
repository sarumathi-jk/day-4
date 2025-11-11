import requests
from app.config import settings

# Hugging Face Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_query_embedding(query: str) -> list[float]:
    """
    Generate an embedding for a query string using Hugging Face Inference API.
    """
    url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{EMBEDDING_MODEL}"
    headers = {"Authorization": f"Bearer {settings.hf_api_key}"}

    response = requests.post(url, headers=headers, json={"inputs": query})
    response.raise_for_status()
    embedding = response.json()

    # Average pooling if nested embeddings
    if isinstance(embedding[0], list):
        embedding = [sum(col) / len(col) for col in zip(*embedding)]

    return embedding


def embed_text_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Embed a list of text chunks for storage in the vector DB.
    """
    embeddings = []
    for chunk in chunks:
        emb = get_query_embedding(chunk)
        embeddings.append(emb)
    return embeddings
