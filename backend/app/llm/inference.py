from __future__ import annotations

import os

import requests

from .prompts import build_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"


def generate_response(
    prompt,
    memory=None,
    facts=None,
    history=None,
    documents=None,
    mode="chat"
):
    model = os.getenv("KAYA_OLLAMA_MODEL", DEFAULT_MODEL)
    ollama_url = os.getenv("KAYA_OLLAMA_URL", OLLAMA_URL)

    payload = {
        "model": model,
        "prompt": build_prompt(
            user_message=prompt,
            memory=memory,
            facts=facts,
            history=history,
            documents=documents,
            mode=mode,
        ),
        "stream": False,
        "options": {
            "temperature": 0.35,
            "top_p": 0.9,
            "repeat_penalty": 1.08,
        },
    }

    response = requests.post(
        ollama_url,
        json=payload,
        timeout=120
    )
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()
