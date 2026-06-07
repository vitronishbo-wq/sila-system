from __future__ import annotations

from typing import Any, Optional


class EmisClientError(Exception):
    pass


class EmisAuthenticationError(EmisClientError):
    pass


class EmisSyncError(EmisClientError):
    pass


class EmisNotFoundError(EmisClientError):
    pass
