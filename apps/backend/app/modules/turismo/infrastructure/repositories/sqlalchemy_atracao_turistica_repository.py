from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.atracao_turistica_repository_port import AtracaoTuristicaRepositoryPort
from app.modules.turismo.domain.enums import TipoAtracao
from app.modules.turismo.domain.models.atracao_turistica import AtracaoTuristica
from app.modules.turismo.infrastructure.models.atracao_turistica_model import AtracaoTuristicaModel


class SQLAlchemyAtracaoTuristicaRepository(AtracaoTuristicaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self, session: AsyncSession | None = None):
        self.session = session
        self._items: dict[UUID, AtracaoTuristicaModel] = {}

    async def save(self, atracao: AtracaoTuristica) -> AtracaoTuristica:
        model = AtracaoTuristicaModel(
            id=atracao.id,
            codigo=atracao.codigo,
            nome=atracao.nome,
            tipo=atracao.tipo,
            descricao=atracao.descricao,
            endereco=atracao.endereco,
            municipio=atracao.municipio,
            provincia=atracao.provincia,
            horario_funcionamento=atracao.horario_funcionamento,
            acessivel=atracao.acessivel,
            ativa=atracao.ativa,
            gratuita=atracao.gratuita,
            capacidade_visitantes_dia=atracao.capacidade_visitantes_dia,
            valor_entrada=atracao.valor_entrada,
            latitude=atracao.latitude,
            longitude=atracao.longitude,
            observacoes=atracao.observacoes,
        )
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, atracao_id: UUID) -> AtracaoTuristica | None:
        model = self._items.get(atracao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo: str) -> AtracaoTuristica | None:
        key = codigo.strip().upper()
        for model in self._items.values():
            if model.codigo.upper() == key:
                return self._to_domain(model)
        return None

    async def list(
        self,
        *,
        tipo: TipoAtracao | None = None,
        municipio: str | None = None,
        ativa: bool | None = None,
    ) -> list[AtracaoTuristica]:
        values = list(self._items.values())
        if tipo is not None:
            values = [item for item in values if item.tipo == tipo]
        if municipio is not None:
            target = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == target]
        if ativa is not None:
            values = [item for item in values if item.ativa == ativa]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def delete(self, atracao_id: UUID) -> bool:
        if atracao_id not in self._items:
            return False
        del self._items[atracao_id]
        return True

    async def next_codigo(self, provincia: str) -> str:
        sigla = provincia.strip().upper()
        ano = date.today().year
        prefixo = f"AT/{sigla}/{ano}/"
        sequencia = sum(1 for item in self._items.values() if item.codigo.startswith(prefixo)) + 1
        return f"AT/{sigla}/{ano}/{sequencia:04d}"

    @staticmethod
    def _to_domain(model: AtracaoTuristicaModel) -> AtracaoTuristica:
        return AtracaoTuristica(
            id=model.id,
            codigo=model.codigo,
            nome=model.nome,
            tipo=model.tipo,
            descricao=model.descricao,
            endereco=model.endereco,
            municipio=model.municipio,
            provincia=model.provincia,
            horario_funcionamento=model.horario_funcionamento,
            acessivel=model.acessivel,
            ativa=model.ativa,
            gratuita=model.gratuita,
            capacidade_visitantes_dia=model.capacidade_visitantes_dia,
            valor_entrada=model.valor_entrada,
            latitude=model.latitude,
            longitude=model.longitude,
            observacoes=model.observacoes,
        )
