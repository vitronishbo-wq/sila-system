import os
import json
import requests
from dotenv import load_dotenv

# Load .env variables (already used by main app too)
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1/responses"


def generate_text(prompt: str, model: str = "gpt-5-nano") -> dict:
    """Call OpenAI Responses API and return parsed JSON.

    Raises RuntimeError if API key is not configured or HTTP errors occur.
    """
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY não definido no .env")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model": model,
        "input": prompt,
        "store": True,
    }

    resp = requests.post(
        BASE_URL, headers=headers, data=json.dumps(payload), timeout=30
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    prompt = "escreva um haicai sobre programação"
    result = generate_text(prompt)
    print(json.dumps(result, indent=2, ensure_ascii=False))
