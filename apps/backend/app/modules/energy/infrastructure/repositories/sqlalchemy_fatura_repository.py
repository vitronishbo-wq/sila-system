from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import FaturaRepositoryPort
from apps.backend.app.modules.energy.domain.enums import StatusFaturaEnergia
from apps.backend.app.modules.energy.domain.models import FaturaEnergia
from apps.backend.app.modules.energy.infrastructure.models import FaturaEnergiaModel

class SQLAlchemyFaturaRepository(FaturaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, FaturaEnergiaModel] = {}
        self._idx_numero: dict[str, UUID] = {}
        self._seq = 0

    async def save(self, item: FaturaEnergia) -> FaturaEnergia:
        model = FaturaEnergiaModel(id=item.id, numero_fatura=item.numero_fatura, consumo_id=item.consumo_id, unidade_consumidora_id=item.unidade_consumidora_id, cpf_titular=item.cpf_titular, mes_referencia=item.mes_referencia, consumo_kwh=item.consumo_kwh, tarifa_kwh=item.tarifa_kwh, bandeira_tarifaria=item.bandeira_tarifaria, valor_consumo=item.valor_consumo, valor_bandeira=item.valor_bandeira, valor_iluminacao_publica=item.valor_iluminacao_publica, valor_total=item.valor_total, data_emissao=item.data_emissao, data_vencimento=item.data_vencimento, status=item.status, data_pagamento=item.data_pagamento, valor_pago=item.valor_pago, metodo_pagamento=item.metodo_pagamento)
        self._items[model.id] = model
        self._idx_numero[model.numero_fatura] = model.id
        return self._to_domain(model)

    async def get_by_id(self, fatura_id: UUID) -> FaturaEnergia | None:
        model = self._items.get(fatura_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_fatura: str) -> FaturaEnergia | None:
        idx = self._idx_numero.get(numero_fatura.strip())
        if not idx:
            return None
        model = self._items.get(idx)
        return self._to_domain(model) if model else None

    async def list(self, *, unidade_consumidora_id: UUID | None=None, cpf_titular: str | None=None, status: StatusFaturaEnergia | None=None) -> list[FaturaEnergia]:
        values = list(self._items.values())
        if unidade_consumidora_id:
            values = [item for item in values if item.unidade_consumidora_id == unidade_consumidora_id]
        if cpf_titular:
            normalized = cpf_titular.strip()
            values = [item for item in values if item.cpf_titular == normalized]
        if status:
            values = [item for item in values if item.status == status]
        values.sort(key=lambda item: item.data_emissao, reverse=True)
        return [self._to_domain(item) for item in values]

    async def next_numero(self) -> str:
        self._seq += 1
        return f'ENE/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: FaturaEnergiaModel) -> FaturaEnergia:
        return FaturaEnergia(id=model.id, numero_fatura=model.numero_fatura, consumo_id=model.consumo_id, unidade_consumidora_id=model.unidade_consumidora_id, cpf_titular=model.cpf_titular, mes_referencia=model.mes_referencia, consumo_kwh=Decimal(model.consumo_kwh), tarifa_kwh=Decimal(model.tarifa_kwh), bandeira_tarifaria=model.bandeira_tarifaria, valor_consumo=Decimal(model.valor_consumo), valor_bandeira=Decimal(model.valor_bandeira), valor_iluminacao_publica=Decimal(model.valor_iluminacao_publica), valor_total=Decimal(model.valor_total), data_emissao=model.data_emissao, data_vencimento=model.data_vencimento, status=model.status, data_pagamento=model.data_pagamento, valor_pago=Decimal(model.valor_pago) if model.valor_pago is not None else None, metodo_pagamento=model.metodo_pagamento)