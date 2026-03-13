from __future__ import annotations

class CQRSRegistry:
    commands: dict[type, object] = {}
    queries: dict[type, object] = {}

    @classmethod
    def register_command(cls, command_type, handler) -> None:
        cls.commands[command_type] = handler

    @classmethod
    def register_query(cls, query_type, handler) -> None:
        cls.queries[query_type] = handler