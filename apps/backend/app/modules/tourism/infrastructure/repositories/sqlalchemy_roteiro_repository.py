from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.roteiro_repository_port import RoteiroRepositoryPort
from apps.backend.app.modules.tourism.domain.models.roteiro import Roteiro
from apps.backend.app.modules.tourism.infrastructure.models.roteiro_model import RoteiroModel

class SQLAlchemyRoteiroRepository(RoteiroRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self, session: AsyncSession | None=None):
        self.session = session
        self._items: dict[UUID, RoteiroModel] = {}

    async def save(self, roteiro: Roteiro) -> Roteiro:
        model = RoteiroModel(id=roteiro.id, codigo=roteiro.codigo, titulo=roteiro.titulo, descricao=roteiro.descricao, municipio_origem=roteiro.municipio_origem, provincia_origem=roteiro.provincia_origem, duracao_horas=roteiro.duracao_horas, pontos_parada=list(roteiro.pontos_parada), acessivel=roteiro.acessivel, ativo=roteiro.ativo, valor_estimado=roteiro.valor_estimado, meios_transporte_sugeridos=list(roteiro.meios_transporte_sugeridos or []), parceiros_comerciais=list(roteiro.parceiros_comerciais or []), observacoes=roteiro.observacoes)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, roteiro_id: UUID) -> Roteiro | None:
        model = self._items.get(roteiro_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo: str) -> Roteiro | None:
        key = codigo.strip().upper()
        for model in self._items.values():
            if model.codigo.upper() == key:
                return self._to_domain(model)
        return None

    async def list(self, *, municipio_origem: str | None=None, ativo: bool | None=None) -> list[Roteiro]:
        values = list(self._items.values())
        if municipio_origem is not None:
            target = municipio_origem.strip().lower()
            values = [item for item in values if item.municipio_origem.lower() == target]
        if ativo is not None:
            values = [item for item in values if item.ativo == ativo]
        values.sort(key=lambda item: item.titulo.lower())
        return [self._to_domain(item) for item in values]

    async def delete(self, roteiro_id: UUID) -> bool:
        if roteiro_id not in self._items:
            return False
        del self._items[roteiro_id]
        return True

    async def next_codigo(self, provincia: str) -> str:
        sigla = provincia.strip().upper()
        ano = date.today().year
        prefixo = f'RT/{sigla}/{ano}/'
        sequencia = sum((1 for item in self._items.values() if item.codigo.startswith(prefixo))) + 1
        return f'RT/{sigla}/{ano}/{sequencia:04d}'

    @staticmethod
    def _to_domain(model: RoteiroModel) -> Roteiro:
        return Roteiro(id=model.id, codigo=model.codigo, titulo=model.titulo, descricao=model.descricao, municipio_origem=model.municipio_origem, provincia_origem=model.provincia_origem, duracao_horas=model.duracao_horas, pontos_parada=list(model.pontos_parada), acessivel=model.acessivel, ativo=model.ativo, valor_estimado=model.valor_estimado, meios_transporte_sugeridos=list(model.meios_transporte_sugeridos or []), parceiros_comerciais=list(model.parceiros_comerciais or []), observacoes=model.observacoes)