"""Energy infrastructure package.

Keep repository imports lazy to avoid side effects during model registration.
"""
from importlib import import_module
from typing import Any

__all__ = [
    "SQLAlchemyUsinaRepository",
    "SQLAlchemyCentralGeradoraRepository",
    "SQLAlchemySubestacaoRepository",
    "SQLAlchemyLinhaTransmissaoRepository",
]


def __getattr__(name: str) -> Any:
    if name in __all__:
        module = import_module("app.modules.energy.core.infrastructure.repositories")
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
