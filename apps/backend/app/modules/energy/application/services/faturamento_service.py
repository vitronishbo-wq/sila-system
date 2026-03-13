from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.application.events.definitions import FaturaGeradaEvent
from apps.backend.app.modules.energy.application.ports import ConsumoRepositoryPort, FaturaRepositoryPort, ONSServicePort, OutboxRepositoryPort
from apps.backend.app.modules.energy.domain.enums import BandeiraTarifaria, StatusFaturaEnergia
from apps.backend.app.modules.energy.domain.models import FaturaEnergia
from apps.backend.app.modules.energy.domain.exceptions import ConsumoNotFoundError, FaturaEnergiaAlreadyExistsError, FaturaEnergiaNotFoundError
from apps.backend.app.modules.energy.infrastructure.persistence.repository import BaseOutboxRepository

class FaturamentoService:

    def __init__(self, *, fatura_repo: FaturaRepositoryPort, consumo_repo: ConsumoRepositoryPort, outbox_repo: OutboxRepositoryPort | None=None, ons_adapter: ONSServicePort | None=None) -> None:
        self._fatura_repo = fatura_repo
        self._consumo_repo = consumo_repo
        self._ons_adapter = ons_adapter
        self._outbox = BaseOutboxRepository(outbox_repo=outbox_repo)

    def has_ons_adapter(self) -> bool:
        return self._ons_adapter is not None

    async def gerar_fatura_por_consumo(self, consumo_id: UUID, *, data_referencia: date | None=None) -> FaturaEnergia:
        consumo = await self._consumo_repo.get_by_id(consumo_id)
        if not consumo:
            raise ConsumoNotFoundError('Consumo nao encontrado')
        existentes = await self._fatura_repo.list()
        if any((item.consumo_id == consumo_id and item.status != StatusFaturaEnergia.CANCELADA for item in existentes)):
            raise FaturaEnergiaAlreadyExistsError('Fatura ativa ja gerada para o consumo')
        ref_date = data_referencia or consumo.data_leitura.date()
        mes_ref = f'{ref_date.year}-{ref_date.month:02d}'
        bandeira = await self._obter_bandeira()
        tarifa = self._get_tarifa(consumo.classe_tarifaria)
        fatura = FaturaEnergia.gerar(consumo_id=consumo.id, unidade_consumidora_id=consumo.unidade_consumidora_id, cpf_titular=consumo.cpf_titular, mes_referencia=mes_ref, consumo_kwh=consumo.consumo_periodo_kwh, tarifa_kwh=tarifa, bandeira_tarifaria=bandeira, data_vencimento=ref_date + timedelta(days=15))
        fatura.numero_fatura = await self._fatura_repo.next_numero()
        saved = await self._outbox.commit_with_event(persist=self._fatura_repo.save(fatura), event=FaturaGeradaEvent.from_fatura(fatura))
        return saved

    async def registrar_pagamento(self, numero_fatura: str, *, data_pagamento: date, valor_pago: Decimal, metodo_pagamento: str) -> FaturaEnergia:
        item = await self._fatura_repo.get_by_numero(numero_fatura)
        if not item:
            raise FaturaEnergiaNotFoundError('Fatura nao encontrada')
        item.registrar_pagamento(data_pagamento=data_pagamento, valor_pago=valor_pago, metodo_pagamento=metodo_pagamento)
        return await self._fatura_repo.save(item)

    async def obter_por_numero(self, numero_fatura: str) -> FaturaEnergia:
        item = await self._fatura_repo.get_by_numero(numero_fatura)
        if not item:
            raise FaturaEnergiaNotFoundError('Fatura nao encontrada')
        if item.status == StatusFaturaEnergia.PENDENTE and date.today() > item.data_vencimento:
            item.status = StatusFaturaEnergia.VENCIDA
            item = await self._fatura_repo.save(item)
        return item

    async def listar(self, *, unidade_consumidora_id: UUID | None=None, cpf_titular: str | None=None, status: StatusFaturaEnergia | None=None) -> list[FaturaEnergia]:
        items = await self._fatura_repo.list(unidade_consumidora_id=unidade_consumidora_id, cpf_titular=cpf_titular, status=status)
        updated: list[FaturaEnergia] = []
        for item in items:
            if item.status == StatusFaturaEnergia.PENDENTE and date.today() > item.data_vencimento:
                item.status = StatusFaturaEnergia.VENCIDA
                item = await self._fatura_repo.save(item)
            updated.append(item)
        return updated

    async def _obter_bandeira(self) -> BandeiraTarifaria:
        if self._ons_adapter is None:
            return BandeiraTarifaria.VERDE
        try:
            return await self._ons_adapter.get_bandeira_tarifaria()
        except Exception:
            return BandeiraTarifaria.VERDE

    @staticmethod
    def _get_tarifa(classe_tarifaria: str) -> Decimal:
        tarifas = {'b1': Decimal('0.75'), 'b2': Decimal('0.60'), 'b3': Decimal('0.85'), 'a4': Decimal('0.65'), 'a3': Decimal('0.62'), 'a2': Decimal('0.60'), 'a1': Decimal('0.58')}
        return tarifas.get(classe_tarifaria.strip().lower(), Decimal('0.75'))
