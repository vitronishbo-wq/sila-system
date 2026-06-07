"""
Platform — SILA Governance Platform.

This directory shadows Python's stdlib 'platform' package by design.
We bridge stdlib attributes transparently so libraries like sqlalchemy
that do 'import platform; platform.python_implementation()' work.
"""
import importlib.util as _util
import sys as _sys
import types as _types

# --- Load the stdlib platform module directly via its file path ---
_stdlib_spec = _util.find_spec('platform')
if _stdlib_spec and _stdlib_spec.origin and 'site-packages' not in _stdlib_spec.origin:
    # Found stdlib platform (origin will be like /usr/lib/python3.x/platform.py)
    _stdlib = _util.module_from_spec(_stdlib_spec)
    _stdlib_spec.loader.exec_module(_stdlib)
    # Copy all stdlib attributes into this module's namespace
    for _attr in dir(_stdlib):
        if not _attr.startswith('_'):
            globals()[_attr] = getattr(_stdlib, _attr)

# Remove helper artifacts
del _attr, _stdlib, _stdlib_spec, _util, _types
