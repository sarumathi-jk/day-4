from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.document_loader import load_document_text
from app.utils.text_splitter import chunk_text
from app.services.embedding_service import embed_text_chunks
from app.services.vector_store_service import upsert_documents

router = APIRouter()


@router.post("/file")
async def upload_legal_file(file: UploadFile = File(...)):
    """
    Upload a PDF or text legal document.
    1️⃣ Extracts text
    2️⃣ Splits into chunks
    3️⃣ Embeds and stores in vector database
    """
    try:
        # Step 1: Extract text
        text = await load_document_text(file)

        # Step 2: Split into chunks
        chunks = chunk_text(text)

        # Step 3: Embed and store
        embeddings = embed_text_chunks(chunks)
        upsert_documents(chunks, embeddings)

        return {"status": "success", "message": f"Indexed {len(chunks)} chunks from {file.filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
