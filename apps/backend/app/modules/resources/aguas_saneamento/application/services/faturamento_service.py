from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.resources.aguas_saneamento.application.events.fatura_events import FaturaEmitidaEvent, FaturaPagamentoRegistradoEvent
from app.modules.resources.aguas_saneamento.application.ports.fatura_repository_port import FaturaRepositoryPort
from app.modules.resources.aguas_saneamento.application.ports.outbox_repository_port import OutboxRepositoryPort
from app.modules.resources.aguas_saneamento.domain.enums import MetodoPagamento, StatusFatura
from app.modules.resources.aguas_saneamento.domain.models.fatura_agua import FaturaAgua
from app.modules.resources.aguas_saneamento.exceptions import FaturaAlreadyExistsError, FaturaNotFoundError
from app.modules.resources.aguas_saneamento.infrastructure.persistence.repository import BaseOutboxRepository

class FaturamentoService:

    def __init__(self, *, fatura_repo: FaturaRepositoryPort, outbox_repo: OutboxRepositoryPort | None=None) -> None:
        self._fatura_repo = fatura_repo
        self._outbox = BaseOutboxRepository(outbox_repo=outbox_repo)

    async def emitir(self, *, consumo_id: UUID, titular_id: UUID, referencia: str, volume_m3: Decimal, tarifa_m3: Decimal, data_vencimento: date) -> FaturaAgua:
        existentes = await self._fatura_repo.list(consumo_id=consumo_id, referencia=referencia)
        ativos = {StatusFatura.EMITIDA, StatusFatura.VENCIDA, StatusFatura.PAGA}
        if any((item.status in ativos for item in existentes)):
            raise FaturaAlreadyExistsError('Ja existe fatura ativa para consumo e referencia')
        item = FaturaAgua.emitir(consumo_id=consumo_id, titular_id=titular_id, referencia=referencia, volume_m3=volume_m3, tarifa_m3=tarifa_m3, data_vencimento=data_vencimento)
        item.numero_fatura = await self._fatura_repo.next_numero()
        saved = await self._outbox.commit_with_event(persist=self._fatura_repo.save(item), event=FaturaEmitidaEvent.from_fatura(item))
        return saved

    async def registrar_pagamento(self, numero_fatura: str, *, data_pagamento: date, valor_pago: Decimal, metodo_pagamento: MetodoPagamento) -> FaturaAgua:
        item = await self._obter_ou_erro(numero_fatura)
        item.registrar_pagamento(data_pagamento=data_pagamento, valor_pago=valor_pago, metodo_pagamento=metodo_pagamento)
        saved = await self._outbox.commit_with_event(persist=self._fatura_repo.save(item), event=FaturaPagamentoRegistradoEvent.from_fatura(item))
        return saved

    async def cancelar(self, numero_fatura: str, *, motivo: str) -> FaturaAgua:
        item = await self._obter_ou_erro(numero_fatura)
        item.cancelar(motivo)
        return await self._fatura_repo.save(item)

    async def obter_por_numero(self, numero_fatura: str) -> FaturaAgua:
        item = await self._obter_ou_erro(numero_fatura)
        item.atualizar_status_vencimento()
        return item

    async def listar(self, *, consumo_id: UUID | None=None, titular_id: UUID | None=None, referencia: str | None=None, status: StatusFatura | None=None) -> list[FaturaAgua]:
        items = await self._fatura_repo.list(consumo_id=consumo_id, titular_id=titular_id, referencia=referencia, status=status)
        for item in items:
            item.atualizar_status_vencimento()
        return items

    async def _obter_ou_erro(self, numero_fatura: str) -> FaturaAgua:
        item = await self._fatura_repo.get_by_numero(numero_fatura)
        if not item:
            raise FaturaNotFoundError('Fatura nao encontrada')
        return item