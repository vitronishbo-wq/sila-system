from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.agencia_viagens_repository_port import AgenciaViagensRepositoryPort
from apps.backend.app.modules.tourism.domain.models.agencia_viagens import AgenciaViagens
from apps.backend.app.modules.tourism.infrastructure.models.agencia_viagens_model import AgenciaViagensModel

class SQLAlchemyAgenciaViagensRepository(AgenciaViagensRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self, session: AsyncSession | None=None):
        self.session = session
        self._items: dict[UUID, AgenciaViagensModel] = {}

    async def save(self, agencia: AgenciaViagens) -> AgenciaViagens:
        model = AgenciaViagensModel(id=agencia.id, registro=agencia.registro, nome_fantasia=agencia.nome_fantasia, razao_social=agencia.razao_social, cnpj=agencia.cnpj, email=agencia.email, telefone=agencia.telefone, endereco=agencia.endereco, numero=agencia.numero, bairro=agencia.bairro, municipio=agencia.municipio, provincia=agencia.provincia, cep=agencia.cep, proprietario_id=agencia.proprietario_id, data_registro=agencia.data_registro, ativa=agencia.ativa, especialidades=list(agencia.especialidades or []), site=agencia.site, observacoes=agencia.observacoes)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, agencia_id: UUID) -> AgenciaViagens | None:
        model = self._items.get(agencia_id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> AgenciaViagens | None:
        key = cnpj.strip()
        for model in self._items.values():
            if model.cnpj == key:
                return self._to_domain(model)
        return None

    async def get_by_registro(self, registro: str) -> AgenciaViagens | None:
        key = registro.strip().upper()
        for model in self._items.values():
            if model.registro.upper() == key:
                return self._to_domain(model)
        return None

    async def list(self, *, municipio: str | None=None, ativa: bool | None=None) -> list[AgenciaViagens]:
        values = list(self._items.values())
        if municipio is not None:
            target = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == target]
        if ativa is not None:
            values = [item for item in values if item.ativa == ativa]
        values.sort(key=lambda item: item.nome_fantasia.lower())
        return [self._to_domain(item) for item in values]

    async def delete(self, agencia_id: UUID) -> bool:
        if agencia_id not in self._items:
            return False
        del self._items[agencia_id]
        return True

    async def next_registro(self, provincia: str) -> str:
        sigla = provincia.strip().upper()
        ano = date.today().year
        prefixo = f'AG/{sigla}/{ano}/'
        sequencia = sum((1 for item in self._items.values() if item.registro.startswith(prefixo))) + 1
        return f'AG/{sigla}/{ano}/{sequencia:04d}'

    @staticmethod
    def _to_domain(model: AgenciaViagensModel) -> AgenciaViagens:
        return AgenciaViagens(id=model.id, registro=model.registro, nome_fantasia=model.nome_fantasia, razao_social=model.razao_social, cnpj=model.cnpj, email=model.email, telefone=model.telefone, endereco=model.endereco, numero=model.numero, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, cep=model.cep, proprietario_id=model.proprietario_id, data_registro=model.data_registro, ativa=model.ativa, especialidades=list(model.especialidades or []), site=model.site, observacoes=model.observacoes)