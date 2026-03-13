from __future__ import annotations

class SnapshotManager:

    def __init__(self):
        self.snapshots = {}

    def save(self, aggregate_id, state) -> None:
        self.snapshots[aggregate_id] = state

    def load(self, aggregate_id):
        return self.snapshots.get(aggregate_id)