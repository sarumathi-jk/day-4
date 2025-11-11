from app.config import settings
from typing import List
import pinecone
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

# Global client cache
_vector_client = None


def get_vector_client():
    """
    Initialize and return the correct vector DB client.
    """
    global _vector_client
    if _vector_client is not None:
        return _vector_client

    provider = settings.vector_db_provider.lower()

    if provider == "pinecone":
        pinecone.init(api_key=settings.vector_db_api_key, environment=settings.vector_db_env)
        _vector_client = pinecone.Index(settings.vector_db_index_name)
    elif provider == "qdrant":
        _vector_client = QdrantClient(
            url=settings.vector_db_api_url,
            api_key=settings.vector_db_api_key
        )
    else:
        raise ValueError("Unsupported vector database provider")

    return _vector_client


def upsert_documents(chunks: List[str], embeddings: List[List[float]]):
    """
    Store text chunks + embeddings in the vector DB.
    """
    client = get_vector_client()
    provider = settings.vector_db_provider.lower()

    if provider == "pinecone":
        vectors = [(str(i), embeddings[i], {"text": chunks[i]}) for i in range(len(chunks))]
        client.upsert(vectors=vectors)
    elif provider == "qdrant":
        points = [
            PointStruct(id=i, vector=embeddings[i], payload={"text": chunks[i]})
            for i in range(len(chunks))
        ]
        client.upsert(collection_name=settings.vector_db_collection_name, points=points)


def retrieve_similar_docs(query_embedding: List[float], top_k: int = 3) -> List[str]:
    """
    Retrieve the most relevant legal text chunks for the given query embedding.
    """
    client = get_vector_client()
    provider = settings.vector_db_provider.lower()

    if provider == "pinecone":
        results = client.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [match["metadata"]["text"] for match in results["matches"]]
    elif provider == "qdrant":
        results = client.search(
            collection_name=settings.vector_db_collection_name,
            query_vector=query_embedding,
            limit=top_k,
        )
        return [r.payload["text"] for r in results]
    else:
        return []
