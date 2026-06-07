from __future__ import annotations

from typing import Any
from uuid import UUID


def parse_uuid(value: Any, field_name: str) -> tuple[UUID | None, str | None]:
    """Converte valor para UUID com erro padronizado."""
    if value is None:
        return (None, f"Campo obrigatório ausente: {field_name}")
    try:
        return (UUID(str(value)), None)
    except (TypeError, ValueError):
        return (None, f"UUID inválido para campo '{field_name}'")
