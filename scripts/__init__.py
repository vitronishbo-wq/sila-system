# Package marker to allow importing `scripts.*` from tests and tools
__all__ = []
"""Make the scripts folder importable as a package for tests.

This file intentionally left minimal. It enables imports like
`from scripts.force_delete_users import ...` in test modules.
"""

__all__ = []
