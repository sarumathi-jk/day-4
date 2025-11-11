import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # === App Settings ===
    app_name: str = Field("Legal RAG App", env="APP_NAME")
    app_env: str = Field("development", env="APP_ENV")
    app_port: int = Field(8000, env="APP_PORT")
    log_level: str = Field("info", env="LOG_LEVEL")

    # === Hugging Face ===
    hf_api_key: str = Field(..., env="HUGGINGFACE_API_KEY")
    hf_model_id: str = Field("mistralai/Mistral-7B-Instruct-v0.2", env="HUGGINGFACE_MODEL_ID")

    # === Vector Database (Cloud) ===
    vector_db_provider: str = Field("pinecone", env="VECTOR_DB_PROVIDER")
    vector_db_api_key: str | None = Field(None, env="VECTOR_DB_API_KEY")
    vector_db_api_url: str | None = Field(None, env="VECTOR_DB_API_URL")
    vector_db_env: str | None = Field(None, env="VECTOR_DB_ENV")
    vector_db_index_name: str | None = Field("legal-rag", env="VECTOR_DB_INDEX_NAME")
    vector_db_collection_name: str | None = Field("legal_rag_docs", env="VECTOR_DB_COLLECTION_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate global settings
settings = Settings()

# === Optional: Debug Logging ===
if settings.app_env == "development":
    print(f"✅ Loaded configuration for {settings.app_name}")
    print(f"🧠 Using Hugging Face model: {settings.hf_model_id}")
    print(f"💾 Vector DB Provider: {settings.vector_db_provider}")
