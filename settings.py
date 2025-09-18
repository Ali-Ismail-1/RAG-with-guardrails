# settings.py
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve()

class Settings(BaseSettings):
    # Provider + OpenAI
    llm_provider: str = "ollama" # "openai"

    # OpenAI
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

    # Ollama
    ollama_model: str = "llama3.8b"
    ollama_base_url: str | None = None # default "http://localhost:11434"

    # Documents
    doc_dir: str = str("app/data/docs")

    # Embeddings + Chroma
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_dir: str = str("app/data/chroma")

    # Orchestration toggle
    use_langgraph: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()