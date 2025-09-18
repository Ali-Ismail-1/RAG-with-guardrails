# guardrails/filters.py
import re

_THINK_RE = re.compile(r"<think>(.*?)</think>\s*", re.DOTALL)

def strip_think(text: str) -> str:
    """Remove hidden <think> tags from LLM Outputs"""
    return _THINK_RE.sub("", text).strip()