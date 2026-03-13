from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira
from apps.backend.app.modules.tourism.domain.models.pousada import Pousada
from apps.backend.app.modules.tourism.application.ports.pousada_repository_port import PousadaRepositoryPort
from apps.backend.app.modules.tourism.infrastructure.models.pousada_model import PousadaModel

class SQLAlchemyPousadaRepository(PousadaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self, session: AsyncSession | None=None):
        self.session = session
        self._items: dict[UUID, PousadaModel] = {}

    async def save(self, pousada: Pousada) -> Pousada:
        model = PousadaModel(id=pousada.id, cadastur=pousada.cadastur, nome=pousada.nome, tipo=pousada.tipo, classificacao=pousada.classificacao, cnpj=pousada.cnpj, endereco=pousada.endereco, numero=pousada.numero, bairro=pousada.bairro, municipio=pousada.municipio, provincia=pousada.provincia, cep=pousada.cep, telefone=pousada.telefone, email=pousada.email, quartos=pousada.quartos, capacidade_maxima=pousada.capacidade_maxima, proprietario_id=pousada.proprietario_id, data_abertura=pousada.data_abertura, ativa=pousada.ativa, site=pousada.site, observacoes=pousada.observacoes)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, pousada_id: UUID) -> Pousada | None:
        model = self._items.get(pousada_id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> Pousada | None:
        key = cnpj.strip()
        for model in self._items.values():
            if model.cnpj == key:
                return self._to_domain(model)
        return None

    async def get_by_cadastur(self, cadastur: str) -> Pousada | None:
        key = cadastur.strip().upper()
        for model in self._items.values():
            if model.cadastur.upper() == key:
                return self._to_domain(model)
        return None

    async def list(self, *, municipio: str | None=None, classificacao: ClassificacaoHoteleira | None=None, ativa: bool | None=None) -> list[Pousada]:
        values = list(self._items.values())
        if municipio is not None:
            target = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == target]
        if classificacao is not None:
            values = [item for item in values if item.classificacao == classificacao]
        if ativa is not None:
            values = [item for item in values if item.ativa == ativa]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def delete(self, pousada_id: UUID) -> bool:
        if pousada_id not in self._items:
            return False
        del self._items[pousada_id]
        return True

    async def next_cadastur(self, provincia: str) -> str:
        sigla = provincia.strip().upper()
        ano = date.today().year
        prefixo = f'PO/{sigla}/{ano}/'
        sequencia = sum((1 for item in self._items.values() if item.cadastur.startswith(prefixo))) + 1
        return f'PO/{sigla}/{ano}/{sequencia:04d}'

    @staticmethod
    def _to_domain(model: PousadaModel) -> Pousada:
        return Pousada(id=model.id, cadastur=model.cadastur, nome=model.nome, tipo=model.tipo, classificacao=model.classificacao, cnpj=model.cnpj, endereco=model.endereco, numero=model.numero, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, cep=model.cep, telefone=model.telefone, email=model.email, quartos=model.quartos, capacidade_maxima=model.capacidade_maxima, proprietario_id=model.proprietario_id, data_abertura=model.data_abertura, ativa=model.ativa, site=model.site, observacoes=model.observacoes)
