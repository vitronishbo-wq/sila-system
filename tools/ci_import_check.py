import sys
import json
from pathlib import Path

backend = Path("/opt/sila-system/backend")
if str(backend) not in sys.path:
    sys.path.insert(0, str(backend))

result = {"imported": False, "symbols": {}, "error": None}
try:
    import importlib

    m = importlib.import_module("modules.location.models")
    result["imported"] = True
    for name in ("CommuneCreate", "CommuneResponse", "CommuneUpdate"):
        result["symbols"][name] = hasattr(m, name)
except Exception as e:
    result["error"] = f"{type(e).__name__}: {e}"

print(json.dumps(result, indent=2, ensure_ascii=False))
