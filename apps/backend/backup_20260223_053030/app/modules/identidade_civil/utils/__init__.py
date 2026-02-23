"""
Utilitários do Módulo Identidade Civil
"""

from .safe import (
    safe_get,
    safe_getitem,
    safe_isoformat,
    safe_int,
    safe_float,
    safe_str,
    safe_bool,
    safe_apply,
    safe_or_raise,
)

__all__ = [
    "safe_get",
    "safe_getitem", 
    "safe_isoformat",
    "safe_int",
    "safe_float",
    "safe_str",
    "safe_bool",
    "safe_apply",
    "safe_or_raise",
]
