from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embedding_service import get_query_embedding
from app.services.vector_store_service import retrieve_similar_docs
from app.services.llm_service import generate_answer

router = APIRouter()

# Request schema
class RAGQuery(BaseModel):
    query: str

# Response schema
class RAGResponse(BaseModel):
    query: str
    context: list[str]
    answer: str


@router.post("/query", response_model=RAGResponse)
async def rag_query(request: RAGQuery):
    """
    Handle a user's legal query using RAG flow:
    1️⃣ Embed query
    2️⃣ Retrieve relevant documents from vector DB
    3️⃣ Generate grounded answer using Hugging Face model
    """
    try:
        # Step 1: Embed query
        query_embedding = get_query_embedding(request.query)

        # Step 2: Retrieve top matching docs
        context_docs = retrieve_similar_docs(query_embedding, top_k=3)

        # Step 3: Generate final answer
        answer = generate_answer(request.query, context_docs)

        return RAGResponse(
            query=request.query,
            context=context_docs,
            answer=answer
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {e}")
