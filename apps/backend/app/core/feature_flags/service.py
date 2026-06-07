"""Simple env-backed feature flag service."""

import os


class FeatureFlagService:
    def __init__(self, prefix: str = "SILA_FF_"):
        self.prefix = prefix
        self._overrides: dict[str, bool] = {}

    def set(self, flag: str, enabled: bool) -> None:
        self._overrides[flag.upper()] = enabled

    def is_enabled(self, flag: str, default: bool = False) -> bool:
        normalized = flag.upper()
        if normalized in self._overrides:
            return self._overrides[normalized]
        raw = os.getenv(f"{self.prefix}{normalized}")
        if raw is None:
            return default
        return raw.strip().lower() in {"1", "true", "yes", "on", "enabled"}
