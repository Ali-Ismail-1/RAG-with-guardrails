# llm/providers.py
import os
from settings import settings

def get_llm():
    provider = os.getenv("llm_provider", "openai").lower()

    if provider == "openai":
        # Import only when needed
        from langchain_openai import ChatOpenAI
        # Optional: support OpenAI-compatible bases (Groq/OpenRouter) via env
        base_url = os.getenv("OPENAI_BASE_URL")  # e.g., https://api.groq.com/openai/v1
        return ChatOpenAI(
            model=settings.openai_model,
            temperature=0.1,
            api_key=settings.openai_api_key,
            base_url=base_url,
        )

    if provider == "ollama":
        # Import only when needed, and give a helpful error if missing
        try:
            from langchain_ollama import ChatOllama
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "llm_provider=ollama but 'langchain-ollama' is not installed in this environment. "
                "Install it (pip install langchain-ollama) or set llm_provider=openai."
            ) from e

        kwargs = {}
        if settings.ollama_base_url:
            kwargs["base_url"] = settings.ollama_base_url  # e.g., http://host.docker.internal:11434 (Docker) or http://localhost:11434
        return ChatOllama(
            model=settings.ollama_model,
            temperature=0.1,
            **kwargs,
        )

    raise ValueError(f"Invalid LLM provider: {provider}")
