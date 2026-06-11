"""Compatibility shim for `modules.society.educacao.infrastructure`.
Re-exports the canonical `modules.educacao.infrastructure` package.
"""

from apps.backend.app.modules.educacao import infrastructure as _infrastructure

__all__ = ["_infrastructure"]
