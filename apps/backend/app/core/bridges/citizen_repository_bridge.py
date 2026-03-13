"""Citizen repository bridge.

Provides a stable import path for the canonical citizen repository adapter.
"""
from __future__ import annotations
import importlib
from typing import Any

class CitizenRepository:
    """Lazy bridge that resolves the canonical repository at runtime."""

    def __new__(cls, *args: Any, **kwargs: Any):
        module = importlib.import_module('app.modules.justice.civil_registry.infrastructure.repositories.citizen_repository')
        canonical_cls = getattr(module, 'CitizenRepository')
        return canonical_cls(*args, **kwargs)
__all__ = ['CitizenRepository']