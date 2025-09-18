# guardrails/filters.py
import re

_THINK_RE = re.compile(r"<think>(.*?)</think>\s*", re.DOTALL)

PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), # SSN
    # Phone
    re.compile(r"\b\d{3}-\d{3}-\d{4}\b"), # Phone
    # Email
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), # Email
]

PROFANITY_WORDS = {
    "dagnabbit",
    "darn",
    "heck",
    "shoot",
    "sugarplums",
    "frickin",
}

PROFANITY_PATTERNS = [re.compile(rf"\b{word}\b", re.IGNORECASE) for word in PROFANITY_WORDS]

def strip_think(text: str) -> str:
    """Remove hidden <think> tags from LLM Outputs"""
    return _THINK_RE.sub("", text).strip()

def redact_pii(text: str) -> str:
    """Redact PII from text"""
    for pattern in PII_PATTERNS:
        text = pattern.sub("REDACTED", text)
    return text

def contains_profanity(text: str) -> bool:
    """Check if text contains profanity"""
    return any(pattern.search(text) for pattern in PROFANITY_PATTERNS)