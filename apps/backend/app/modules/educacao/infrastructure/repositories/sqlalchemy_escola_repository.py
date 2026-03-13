from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.educacao.application.ports import EscolaRepositoryPort
from apps.backend.app.modules.educacao.domain.models import CicloEnsino, Escola, TipoEscola
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel

class SQLAlchemyEscolaRepository(EscolaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, escola: Escola) -> Escola:
        model = await self.session.get(EscolaModel, escola.id)
        if not model:
            model = EscolaModel(id=escola.id)
            self.session.add(model)
        model.codigo_med = escola.codigo_med
        model.nome = escola.nome
        model.tipo = escola.tipo.value
        model.ciclos = [c.value for c in escola.ciclos]
        model.provincia = escola.provincia
        model.municipio = escola.municipio
        model.comuna = escola.comuna
        model.bairro = escola.bairro
        model.endereco = escola.endereco
        model.contacto = escola.contacto
        model.email = escola.email
        model.ativa = escola.ativa
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id):
        model = await self.session.get(EscolaModel, id)
        return self._to_domain(model) if model else None

    async def get_by_codigo_med(self, codigo_med: str):
        stmt = select(EscolaModel).where(EscolaModel.codigo_med == codigo_med)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_filters(self, provincia=None, municipio=None, tipo: TipoEscola | None=None, ciclo: CicloEnsino | None=None, ativa: bool | None=None) -> list[Escola]:
        stmt = select(EscolaModel)
        if provincia is not None:
            stmt = stmt.where(EscolaModel.provincia == provincia)
        if municipio is not None:
            stmt = stmt.where(EscolaModel.municipio == municipio)
        if tipo is not None:
            stmt = stmt.where(EscolaModel.tipo == tipo.value)
        if ciclo is not None:
            stmt = stmt.where(EscolaModel.ciclos.contains([ciclo.value]))
        if ativa is not None:
            stmt = stmt.where(EscolaModel.ativa == ativa)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(model: EscolaModel) -> Escola:
        return Escola(id=model.id, codigo_med=model.codigo_med, nome=model.nome, tipo=TipoEscola(model.tipo), ciclos=[CicloEnsino(item) for item in model.ciclos or []], provincia=model.provincia, municipio=model.municipio, comuna=model.comuna, bairro=model.bairro, endereco=model.endereco, contacto=model.contacto, email=model.email, ativa=model.ativa)