import importlib
from fastapi.testclient import TestClient


# Import the FastAPI app from the project's main module
app_mod = importlib.import_module("apps.backend.main")
app = app_mod.app
client = TestClient(app)


def test_codex_endpoint_monkeypatched(monkeypatch):
    # Import the openai endpoints module and patch the generate_text function used there
    import sys

    # prefer the module name used by the running app; main imports under 'modules.*'
    endpoints_mod = sys.modules.get(
        "apps.backend.modules.openai.endpoints"
    ) or sys.modules.get("modules.openai.endpoints")
    if endpoints_mod is None:
        # fall back to importing under the app package path
        endpoints_mod = importlib.import_module("apps.backend.modules.openai.endpoints")

    def fake_generate_text(prompt, model=None):
        return {"ok": True, "prompt": prompt, "model": model}

    monkeypatch.setattr(endpoints_mod, "generate_text", fake_generate_text)

    resp = client.post("/api/v1/openai/codex", json={"prompt": "hello test"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["prompt"] == "hello test"
    assert body["ok"] is True
