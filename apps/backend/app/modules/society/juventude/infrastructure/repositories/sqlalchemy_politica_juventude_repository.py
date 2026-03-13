from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.juventude.application.ports.politica_juventude_repository_port import PoliticaJuventudeRepositoryPort
from app.modules.society.juventude.domain.enums import AreaInteresse, StatusPoliticaJuventude
from app.modules.society.juventude.domain.models.politica_juventude import PoliticaJuventude
from app.modules.society.juventude.infrastructure.models.politica_juventude_model import PoliticaJuventudeModel

class SQLAlchemyPoliticaJuventudeRepository(PoliticaJuventudeRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, politica: PoliticaJuventude) -> PoliticaJuventude:
        model = await self.session.get(PoliticaJuventudeModel, politica.id)
        if not model:
            model = PoliticaJuventudeModel(id=politica.id)
            self.session.add(model)
        model.codigo_politica = politica.codigo_politica
        model.nome = politica.nome
        model.descricao = politica.descricao
        model.area_interesse = politica.area_interesse.value
        model.data_inicio = politica.data_inicio
        model.data_fim = politica.data_fim
        model.status = politica.status.value
        model.metas = politica.metas
        model.indicadores = politica.indicadores
        model.data_cadastro = politica.data_cadastro
        model.observacoes = politica.observacoes
        model.ativa = politica.ativa
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, politica_id: UUID) -> PoliticaJuventude | None:
        model = await self.session.get(PoliticaJuventudeModel, politica_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_politica: str) -> PoliticaJuventude | None:
        stmt = select(PoliticaJuventudeModel).where(PoliticaJuventudeModel.codigo_politica == codigo_politica.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[PoliticaJuventude]:
        stmt = select(PoliticaJuventudeModel).order_by(PoliticaJuventudeModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusPoliticaJuventude) -> list[PoliticaJuventude]:
        stmt = select(PoliticaJuventudeModel).where(PoliticaJuventudeModel.status == status.value).order_by(PoliticaJuventudeModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_area(self, area: AreaInteresse) -> list[PoliticaJuventude]:
        stmt = select(PoliticaJuventudeModel).where(PoliticaJuventudeModel.area_interesse == area.value).order_by(PoliticaJuventudeModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, politica_id: UUID) -> bool:
        model = await self.session.get(PoliticaJuventudeModel, politica_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(PoliticaJuventudeModel).where(PoliticaJuventudeModel.codigo_politica.like(f'POL/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'POL/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: PoliticaJuventudeModel) -> PoliticaJuventude:
        return PoliticaJuventude(id=model.id, codigo_politica=model.codigo_politica, nome=model.nome, descricao=model.descricao, area_interesse=AreaInteresse(model.area_interesse), data_inicio=model.data_inicio, data_fim=model.data_fim, status=StatusPoliticaJuventude(model.status), metas=model.metas, indicadores=model.indicadores, data_cadastro=model.data_cadastro or date.today(), observacoes=model.observacoes, ativa=model.ativa)