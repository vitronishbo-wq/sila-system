"""Smoke test: import location models and check exported names.

This test is intentionally minimal: it prevents regressions where
`modules.location.models` fails to expose expected Pydantic models due to
import/package conflicts.
"""

import importlib


def test_location_models_exports():
    m = importlib.import_module("modules.location.models")
    # basic symbols we expect to be re-exported by the shim
    expected = {"CommuneCreate", "CommuneUpdate", "CommuneResponse"}
    available = set(n for n in dir(m) if not n.startswith("_"))
    missing = expected - available
    assert (
        not missing
    ), f"Missing exported names in modules.location.models: {sorted(missing)}"
