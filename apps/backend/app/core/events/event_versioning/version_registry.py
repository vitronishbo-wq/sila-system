from __future__ import annotations


class EventVersionRegistry:
    versions: dict[tuple[str, str], object] = {}

    @classmethod
    def register(cls, event_name, version, transformer) -> None:
        cls.versions[event_name, version] = transformer

    @classmethod
    def get(cls, event_name, version):
        return cls.versions.get((event_name, version))
