# settings.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Provider + OpenAI
    llm_provider: str = "ollama" # "openai"

    # OpenAI
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

    # Ollama
    ollama_model: str = "llama3.8b"
    ollama_base_url: str | None = None # default "http://localhost:11434"

    # Embeddings + Chroma
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_dir: str = "app/data/chroma"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()