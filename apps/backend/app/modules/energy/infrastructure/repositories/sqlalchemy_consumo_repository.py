from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import ConsumoRepositoryPort
from apps.backend.app.modules.energy.domain.models import ConsumoEnergia
from apps.backend.app.modules.energy.infrastructure.models import ConsumoEnergiaModel

class SQLAlchemyConsumoRepository(ConsumoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, ConsumoEnergiaModel] = {}

    async def save(self, item: ConsumoEnergia) -> ConsumoEnergia:
        model = ConsumoEnergiaModel(id=item.id, unidade_consumidora_id=item.unidade_consumidora_id, medidor_id=item.medidor_id, data_leitura=item.data_leitura, leitura_kwh=item.leitura_kwh, leitura_anterior_kwh=item.leitura_anterior_kwh, consumo_periodo_kwh=item.consumo_periodo_kwh, tipo_leitura=item.tipo_leitura, classe_tarifaria=item.classe_tarifaria, cpf_titular=item.cpf_titular)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, consumo_id: UUID) -> ConsumoEnergia | None:
        model = self._items.get(consumo_id)
        return self._to_domain(model) if model else None

    async def get_last_by_unidade(self, unidade_consumidora_id: UUID) -> ConsumoEnergia | None:
        values = [item for item in self._items.values() if item.unidade_consumidora_id == unidade_consumidora_id]
        if not values:
            return None
        values.sort(key=lambda item: item.data_leitura, reverse=True)
        return self._to_domain(values[0])

    async def list(self, *, unidade_consumidora_id: UUID | None=None, cpf_titular: str | None=None) -> list[ConsumoEnergia]:
        values = list(self._items.values())
        if unidade_consumidora_id:
            values = [item for item in values if item.unidade_consumidora_id == unidade_consumidora_id]
        if cpf_titular:
            normalized = cpf_titular.strip()
            values = [item for item in values if item.cpf_titular == normalized]
        values.sort(key=lambda item: item.data_leitura, reverse=True)
        return [self._to_domain(item) for item in values]

    @staticmethod
    def _to_domain(model: ConsumoEnergiaModel) -> ConsumoEnergia:
        return ConsumoEnergia(id=model.id, unidade_consumidora_id=model.unidade_consumidora_id, medidor_id=model.medidor_id, data_leitura=model.data_leitura, leitura_kwh=Decimal(model.leitura_kwh), leitura_anterior_kwh=Decimal(model.leitura_anterior_kwh) if model.leitura_anterior_kwh is not None else None, consumo_periodo_kwh=Decimal(model.consumo_periodo_kwh), tipo_leitura=model.tipo_leitura, classe_tarifaria=model.classe_tarifaria, cpf_titular=model.cpf_titular)