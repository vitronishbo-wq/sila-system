from typing import Any


class TransferPolicies:
    """Placeholder for transfer-related policies (config-driven)."""

    def __init__(self, config: dict[str, Any] = None):
        self.config = config or {}

    def get(self, key: str, default=None):
        return self.config.get(key, default)
