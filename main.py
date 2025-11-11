from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import rag, upload

# ======================
# 🚀 FastAPI App Setup
# ======================
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="""
    ⚖️ **Legal RAG Application**

    Retrieval-Augmented Generation (RAG) system for lawyers & advocates:
    - Case law retrieval
    - Contract analysis
    - Legal question answering
    """,
)

# ======================
# 🌍 CORS Configuration
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# 🔌 Route Registration
# ======================
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])

# ======================
# 🏁 Root Endpoint
# ======================
@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.app_name,
        "status": "running ✅",
        "model": settings.hf_model_id,
        "vector_db": settings.vector_db_provider,
    }


# ======================
# 🏃‍♂️ Run Command
# ======================
# Run locally:
# uvicorn app.main:app --reload
