from __future__ import annotations

class PublicBudgetRepository:
    """Lightweight repository facade for budget aggregate persistence."""

    def __init__(self):
        self._store = {}

    def add(self, key, value):
        self._store[key] = value
        return value

    def get(self, key):
        return self._store.get(key)