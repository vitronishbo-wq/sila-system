import sys
from pathlib import Path

backend = Path("/opt/sila-system/backend")
if str(backend) not in sys.path:
    sys.path.insert(0, str(backend))

try:
    import importlib

    m = importlib.import_module("modules.location.models")
    print("Imported modules.location.models OK")
    for name in ("CommuneCreate", "CommuneResponse", "CommuneUpdate"):
        print(f"{name} ->", hasattr(m, name))
except Exception:
    print("IMPORT CHECK FAILED:")
    raise
