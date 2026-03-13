from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.cultura.application.ports.espaco_cultural_repository_port import EspacoCulturalRepositoryPort
from apps.backend.app.modules.society.cultura.domain.enums import TipoEspacoCultural
from apps.backend.app.modules.society.cultura.domain.models.espaco_cultural import EspacoCultural
from apps.backend.app.modules.society.cultura.infrastructure.models.espaco_cultural_model import EspacoCulturalModel

class SQLAlchemyEspacoCulturalRepository(EspacoCulturalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, espaco: EspacoCultural) -> EspacoCultural:
        model = await self.session.get(EspacoCulturalModel, espaco.id)
        if not model:
            model = EspacoCulturalModel(id=espaco.id)
            self.session.add(model)
        model.codigo_espaco = espaco.codigo_espaco
        model.nome = espaco.nome
        model.tipo = espaco.tipo.value
        model.municipio = espaco.municipio
        model.provincia = espaco.provincia
        model.endereco = espaco.endereco
        model.capacidade = espaco.capacidade
        model.area_m2 = espaco.area_m2
        model.administracao = espaco.administracao
        model.responsavel_cpf = espaco.responsavel_cpf
        model.data_registro = espaco.data_registro
        model.orgao_gestor = espaco.orgao_gestor
        model.ano_inauguracao = espaco.ano_inauguracao
        model.acessibilidade = espaco.acessibilidade
        model.visitas_anuais = espaco.visitas_anuais
        model.ativo = espaco.ativo
        model.observacoes = espaco.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, espaco_id: UUID) -> EspacoCultural | None:
        model = await self.session.get(EspacoCulturalModel, espaco_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_espaco: str) -> EspacoCultural | None:
        stmt = select(EspacoCulturalModel).where(EspacoCulturalModel.codigo_espaco == codigo_espaco.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[EspacoCultural]:
        stmt = select(EspacoCulturalModel).order_by(EspacoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoEspacoCultural) -> list[EspacoCultural]:
        stmt = select(EspacoCulturalModel).where(EspacoCulturalModel.tipo == tipo.value).order_by(EspacoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[EspacoCultural]:
        stmt = select(EspacoCulturalModel).where(func.lower(EspacoCulturalModel.municipio) == municipio.strip().lower()).order_by(EspacoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, espaco_id: UUID) -> bool:
        model = await self.session.get(EspacoCulturalModel, espaco_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(EspacoCulturalModel).where(EspacoCulturalModel.codigo_espaco.like(f'ESP/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'ESP/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: EspacoCulturalModel) -> EspacoCultural:
        return EspacoCultural(id=model.id, codigo_espaco=model.codigo_espaco, nome=model.nome, tipo=TipoEspacoCultural(model.tipo), municipio=model.municipio, provincia=model.provincia, endereco=model.endereco, capacidade=model.capacidade, area_m2=model.area_m2, administracao=model.administracao, responsavel_cpf=model.responsavel_cpf, data_registro=model.data_registro, orgao_gestor=model.orgao_gestor, ano_inauguracao=model.ano_inauguracao, acessibilidade=model.acessibilidade, visitas_anuais=model.visitas_anuais, ativo=model.ativo, observacoes=model.observacoes)