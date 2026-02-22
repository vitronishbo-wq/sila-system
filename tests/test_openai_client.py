import importlib
import types
import pytest


def _make_resp(status=200, data=None):
    class Resp:
        def __init__(self, status, data):
            self.status_code = status
            self._data = data or {"ok": True}

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception("HTTP error")

        def json(self):
            return self._data

    return Resp(status, data)


def test_generate_text_success(monkeypatch):
    module_name = "apps.backend.services.openai_client"
    mod = importlib.import_module(module_name)

    # Replace requests.post with a fake that returns a controlled response
    def fake_post(url, headers, data, timeout):
        return _make_resp(200, {"result": "generated text", "input": data})

    # monkeypatch the requests attribute on the imported module
    monkeypatch.setattr(mod, "requests", types.SimpleNamespace(post=fake_post))

    res = mod.generate_text("hello world")
    assert isinstance(res, dict)
    assert res.get("result") == "generated text"


def test_generate_text_no_api_key(monkeypatch):
    # Ensure environment variable is empty and reload module so top-level API_KEY is re-evaluated
    monkeypatch.setenv("OPENAI_API_KEY", "")
    module_name = "apps.backend.services.openai_client"
    mod = importlib.reload(importlib.import_module(module_name))

    with pytest.raises(RuntimeError):
        mod.generate_text("should fail")
