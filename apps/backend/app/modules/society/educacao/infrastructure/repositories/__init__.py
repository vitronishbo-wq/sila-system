"""Compatibility shim for `modules.society.educacao.infrastructure.repositories`.
Re-export required repository classes from the canonical `modules.educacao`.
"""

from apps.backend.app.modules.educacao.infrastructure import repositories as _repos

__all__ = ["_repos"]
