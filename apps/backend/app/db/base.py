from __future__ import annotations

import sys
import types
from collections.abc import Sequence

import app as _app

_apps_module = sys.modules.setdefault("apps", types.ModuleType("apps"))
_backend_module = sys.modules.setdefault("apps.backend", types.ModuleType("apps.backend"))
_apps_module.backend = _backend_module
_backend_module.app = _app
sys.modules.setdefault("apps.backend.app", _app)
from apps.backend.app.core.db import Base


class _LazyModels(Sequence[type]):
    def _load(self) -> list[type]:
        from apps.backend.app.db import registry

        return registry.ALL_MODELS

    def __iter__(self):
        return iter(self._load())

    def __len__(self) -> int:
        return len(self._load())

    def __getitem__(self, index):
        return self._load()[index]

    def __repr__(self) -> str:
        return repr(self._load())


ALL_MODELS = _LazyModels()

__all__ = ["Base", "ALL_MODELS"]
