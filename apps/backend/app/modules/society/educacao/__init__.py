"""Compatibility shim: re-export `modules.educacao` under `modules.society.educacao`.

This keeps older import paths working for bridges and tests that expect
`apps.backend.app.modules.society.educacao...` while the canonical package
is `apps.backend.app.modules.educacao`.
"""

from apps.backend.app.modules import educacao as _educacao

__all__ = ["_educacao"]
