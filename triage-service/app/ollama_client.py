import logging
import os

import httpx

from app.categories import CATEGORIES

logger = logging.getLogger("triage.ollama")

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

# Timeout is generous: CPU inference on commodity hardware can be slow,
# and Assignment 1's baseline is synchronous (POST /tickets waits for it).
_TIMEOUT = httpx.Timeout(120.0, connect=10.0)

_PROMPT_TEMPLATE = """You are a ticket triage classifier for a financial services complaints desk.
Classify the customer complaint narrative below into EXACTLY ONE of these categories:
{categories}

Respond with ONLY the category name, exactly as written above, and nothing else.

Narrative:
\"\"\"{narrative}\"\"\"

Category:"""


def _build_prompt(narrative: str) -> str:
    return _PROMPT_TEMPLATE.format(
        categories="\n".join(f"- {c}" for c in CATEGORIES),
        narrative=narrative,
    )


def _normalize_category(raw: str) -> str:
    """Map the model's free-text reply back onto one of the seven fixed
    categories. Falls back to a substring match, then to the first
    category, so a malformed reply still yields a storable label rather
    than a crash — malformed replies should be visible in the logs
    instead."""
    cleaned = raw.strip().strip('"').strip(".")
    for c in CATEGORIES:
        if cleaned.lower() == c.lower():
            return c
    for c in CATEGORIES:
        if c.lower() in cleaned.lower():
            return c
    logger.warning("Could not match model output to a category: %r", raw)
    return CATEGORIES[0]


def classify(narrative: str, model: str | None = None) -> str:
    """Synchronous call to Ollama's generate endpoint. Baseline behaviour
    per Assignment 1: POST /tickets blocks until this returns."""
    model = model or OLLAMA_MODEL
    prompt = _build_prompt(narrative)

    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0},
            },
        )
        resp.raise_for_status()
        data = resp.json()

    raw = data.get("response", "")
    category = _normalize_category(raw)
    logger.info("Classified ticket with model=%s raw_output=%r category=%s", model, raw, category)
    return category
