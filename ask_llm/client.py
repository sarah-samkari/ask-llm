import json
import requests

from .models import Answer

DEFAULT_MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = (
    "You are a precise assistant. Given a user's question, respond with ONLY a "
    "single JSON object (no markdown fences, no commentary) with exactly these "
    "keys:\n"
    '  "question": string\n'
    '  "answer": string\n'
    '  "confidence": number between 0.0 and 1.0\n'
    '  "reasoning": string\n'
    '  "sources": array of strings\n'
    "Return valid JSON and nothing else."
)


class LLMError(Exception):
    """Raised when the API call fails or the response can't be used."""


def ask_llm(question: str, api_key: str, model: str = DEFAULT_MODEL) -> Answer:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": question}]}],
    }
    headers = {"content-type": "application/json", "x-goog-api-key": api_key}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.exceptions.RequestException as exc:
        raise LLMError(f"Network error calling the LLM API: {exc}") from exc

    if response.status_code != 200:
        raise LLMError(f"API returned HTTP {response.status_code}: {response.text}")

    body = response.json()

    try:
        raw_text = body["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as exc:
        raise LLMError(f"Unexpected API response shape: {body!r}") from exc

    raw_text = _strip_markdown_fence(raw_text)

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise LLMError(f"Model output was not valid JSON: {raw_text}") from exc

    return Answer(**parsed)


def _strip_markdown_fence(text: str) -> str:
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text