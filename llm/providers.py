# llm/providers.py
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from settings import settings

def get_llm():
    import os
    provider = os.getenv("llm_provider", "openai").lower()

    if provider == "ollama":
        kwargs = {}
        if settings.ollama_base_url:
            kwargs["base_url"] = settings.ollama_base_url
        return ChatOllama(model=settings.ollama_model, temperature=0.1, **kwargs)

    elif provider == "openai":
        return ChatOpenAI(model=settings.openai_model, temperature=0.1, api_key=settings.openai_api_key)

    raise ValueError(f"Invalid LLM provider: {provider}")