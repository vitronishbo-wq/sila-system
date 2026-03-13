from __future__ import annotations

from typing import Any, Optional, Protocol
from uuid import UUID


class CitizenRepositoryPort(Protocol):
    async def create(self, citizen: Any, commit: bool = True) -> Any:
        ...

    async def add(self, citizen: Any, commit: bool = True) -> Any:
        ...

    async def update(self, citizen: Any, commit: bool = True) -> Any:
        ...

    async def get_by_id(self, citizen_id: UUID) -> Optional[Any]:
        ...

    async def get_by_bi(self, bi_number: str) -> Optional[Any]:
        ...

    async def get_by_national_id_number(self, national_id_number: str) -> Optional[Any]:
        ...

    async def get_by_nif(self, nif: str) -> Optional[Any]:
        ...

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Any]:
        ...

    async def list(self, *, filters: dict, limit: int, offset: int) -> list[Any]:
        ...

    async def search_by_name(self, name: str, limit: int = 50) -> list[Any]:
        ...

    async def soft_delete(self, citizen_id: UUID) -> None:
        ...

    async def get(self, citizen_id: str) -> Optional[dict[str, Any]]:
        ...


__all__ = ["CitizenRepositoryPort"]
