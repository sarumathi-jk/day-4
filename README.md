# ⚖️ Legal RAG Application – AI Assistant for Lawyers and Advocates

A **Retrieval-Augmented Generation (RAG)** application built with **FastAPI**, designed to assist lawyers and advocates with:
- 🔍 Case law retrieval  
- 🧾 Contract analysis  
- ❓ Legal question answering  

The app integrates **cloud-hosted Hugging Face language models** and a **cloud vector database** (Pinecone, Qdrant Cloud, or Weaviate Cloud) to provide accurate, context-aware legal insights.

---

## 🏗️ Architecture Overview


---

## 🚀 Features

- **Case Law Search:** Upload or connect to a corpus of case laws, search semantically using natural queries.
- **Contract Analysis:** Upload contracts to extract clauses, summarize sections, or highlight risks.
- **Legal QA:** Ask natural-language legal questions and get fact-grounded answers.
- **Cloud-Native:** Uses cloud-hosted vector stores and Hugging Face inference endpoints — no local model weights required.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend API | FastAPI |
| LLM | Cloud-hosted Hugging Face model (e.g., `mistralai/Mistral-7B-Instruct`, `meta-llama/Llama-3-8b`) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (via Hugging Face API) |
| Vector Database | Pinecone / Qdrant Cloud / Weaviate Cloud |
| Data Source | Case law PDFs, contracts, or uploaded legal documents |

---



