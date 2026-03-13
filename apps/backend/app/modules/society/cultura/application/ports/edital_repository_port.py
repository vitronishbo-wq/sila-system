from __future__ import annotations
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.society.cultura.domain.enums import FaseEditalCultural, TipoEditalCultural
from apps.backend.app.modules.society.cultura.domain.models.edital import Edital

class EditalRepositoryPort:

    async def save(self, edital: Edital) -> Edital:
        raise NotImplementedError

    async def get_by_id(self, edital_id: UUID) -> Edital | None:
        raise NotImplementedError

    async def get_by_numero(self, numero: str) -> Edital | None:
        raise NotImplementedError

    async def list_all(self) -> list[Edital]:
        raise NotImplementedError

    async def list_by_tipo(self, tipo: TipoEditalCultural) -> list[Edital]:
        raise NotImplementedError

    async def list_by_fase(self, fase: FaseEditalCultural) -> list[Edital]:
        raise NotImplementedError

    async def list_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[Edital]:
        raise NotImplementedError

    async def find_ativos(self) -> list[Edital]:
        raise NotImplementedError

    async def delete(self, edital_id: UUID) -> bool:
        raise NotImplementedError