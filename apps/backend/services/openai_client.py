"""Minimal OpenAI client wrapper used in tests."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests


API_KEY = os.getenv("OPENAI_API_KEY", "")
API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/responses")


def generate_text(prompt: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")

    payload = {
        "model": model,
        "input": prompt,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        API_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
