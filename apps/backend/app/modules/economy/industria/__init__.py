import importlib
import sys

_target = "apps.backend.app.modules.industry"
_module = importlib.import_module(_target)
sys.modules[__name__] = _module
