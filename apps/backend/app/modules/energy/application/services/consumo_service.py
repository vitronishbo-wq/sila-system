from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.energy.application.events.definitions import LeituraRealizadaEvent
from apps.backend.app.modules.energy.application.ports import (
    ConsumoRepositoryPort,
    OutboxRepositoryPort,
)
from apps.backend.app.modules.energy.domain.enums import TipoLeituraEnergia
from apps.backend.app.modules.energy.domain.exceptions import ConsumoNotFoundError
from apps.backend.app.modules.energy.domain.models import ConsumoEnergia
from apps.backend.app.modules.energy.infrastructure.persistence.repository import (
    BaseOutboxRepository,
)


class ConsumoService:
    def __init__(
        self,
        *,
        consumo_repo: ConsumoRepositoryPort,
        outbox_repo: OutboxRepositoryPort | None = None,
    ) -> None:
        self._consumo_repo = consumo_repo
        self._outbox = BaseOutboxRepository(outbox_repo=outbox_repo)

    async def registrar_leitura(
        self,
        *,
        unidade_consumidora_id: UUID,
        leitura_kwh: Decimal,
        data_leitura: datetime,
        tipo_leitura: TipoLeituraEnergia,
        classe_tarifaria: str,
        cpf_titular: str,
        medidor_id: UUID | None = None,
    ) -> ConsumoEnergia:
        ultimo = await self._consumo_repo.get_last_by_unidade(unidade_consumidora_id)
        leitura_anterior = ultimo.leitura_kwh if ultimo else None
        item = ConsumoEnergia.registrar(
            unidade_consumidora_id=unidade_consumidora_id,
            medidor_id=medidor_id,
            data_leitura=data_leitura,
            leitura_kwh=leitura_kwh,
            leitura_anterior_kwh=leitura_anterior,
            tipo_leitura=tipo_leitura,
            classe_tarifaria=classe_tarifaria,
            cpf_titular=cpf_titular,
        )
        saved = await self._outbox.commit_with_event(
            persist=self._consumo_repo.save(item), event=LeituraRealizadaEvent.from_consumo(item)
        )
        return saved

    async def obter_por_id(self, consumo_id: UUID) -> ConsumoEnergia:
        item = await self._consumo_repo.get_by_id(consumo_id)
        if not item:
            raise ConsumoNotFoundError("Consumo nao encontrado")
        return item

    async def listar(
        self, *, unidade_consumidora_id: UUID | None = None, cpf_titular: str | None = None
    ) -> list[ConsumoEnergia]:
        return await self._consumo_repo.list(
            unidade_consumidora_id=unidade_consumidora_id, cpf_titular=cpf_titular
        )
