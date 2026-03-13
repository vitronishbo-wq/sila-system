from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.juventude.application.ports.programa_repository_port import ProgramaRepositoryPort
from app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma
from app.modules.society.juventude.domain.models.programa_juvenil import ProgramaJuvenil
from app.modules.society.juventude.infrastructure.models.programa_juvenil_model import ProgramaJuvenilModel

class SQLAlchemyProgramaRepository(ProgramaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, programa: ProgramaJuvenil) -> ProgramaJuvenil:
        model = await self.session.get(ProgramaJuvenilModel, programa.id)
        if not model:
            model = ProgramaJuvenilModel(id=programa.id)
            self.session.add(model)
        model.codigo_programa = programa.codigo_programa
        model.nome = programa.nome
        model.tipo = programa.tipo.value
        model.data_inicio = programa.data_inicio
        model.data_fim = programa.data_fim
        model.vagas = programa.vagas
        model.municipio = programa.municipio
        model.provincia = programa.provincia
        model.status = programa.status.value
        model.data_cadastro = programa.data_cadastro
        model.observacoes = programa.observacoes
        model.ativo = programa.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, programa_id: UUID) -> ProgramaJuvenil | None:
        model = await self.session.get(ProgramaJuvenilModel, programa_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_programa: str) -> ProgramaJuvenil | None:
        stmt = select(ProgramaJuvenilModel).where(ProgramaJuvenilModel.codigo_programa == codigo_programa.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[ProgramaJuvenil]:
        stmt = select(ProgramaJuvenilModel).order_by(ProgramaJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoPrograma) -> list[ProgramaJuvenil]:
        stmt = select(ProgramaJuvenilModel).where(ProgramaJuvenilModel.tipo == tipo.value).order_by(ProgramaJuvenilModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusPrograma) -> list[ProgramaJuvenil]:
        stmt = select(ProgramaJuvenilModel).where(ProgramaJuvenilModel.status == status.value).order_by(ProgramaJuvenilModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, programa_id: UUID) -> bool:
        model = await self.session.get(ProgramaJuvenilModel, programa_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(ProgramaJuvenilModel).where(ProgramaJuvenilModel.codigo_programa.like(f'PRG/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PRG/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ProgramaJuvenilModel) -> ProgramaJuvenil:
        return ProgramaJuvenil(id=model.id, codigo_programa=model.codigo_programa, nome=model.nome, tipo=TipoPrograma(model.tipo), data_inicio=model.data_inicio, data_fim=model.data_fim, vagas=model.vagas, municipio=model.municipio, provincia=model.provincia, status=StatusPrograma(model.status), data_cadastro=model.data_cadastro, observacoes=model.observacoes, ativo=model.ativo)