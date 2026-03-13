from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.juventude.application.ports.estagio_juvenil_repository_port import EstagioJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusEstagio
from apps.backend.app.modules.society.juventude.domain.models.estagio_juvenil import EstagioJuvenil
from apps.backend.app.modules.society.juventude.infrastructure.models.estagio_juvenil_model import EstagioJuvenilModel

class SQLAlchemyEstagioJuvenilRepository(EstagioJuvenilRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, estagio: EstagioJuvenil) -> EstagioJuvenil:
        model = await self.session.get(EstagioJuvenilModel, estagio.id)
        if not model:
            model = EstagioJuvenilModel(id=estagio.id)
            self.session.add(model)
        model.codigo_estagio = estagio.codigo_estagio
        model.jovem_id = estagio.jovem_id
        model.instituicao = estagio.instituicao
        model.area_interesse = estagio.area_interesse.value
        model.cargo = estagio.cargo
        model.carga_horaria_semanal = estagio.carga_horaria_semanal
        model.data_inicio = estagio.data_inicio
        model.data_fim = estagio.data_fim
        model.status = estagio.status.value
        model.bolsa_auxilio = estagio.bolsa_auxilio
        model.data_cadastro = estagio.data_cadastro
        model.observacoes = estagio.observacoes
        model.ativo = estagio.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, estagio_id: UUID) -> EstagioJuvenil | None:
        model = await self.session.get(EstagioJuvenilModel, estagio_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_estagio: str) -> EstagioJuvenil | None:
        stmt = select(EstagioJuvenilModel).where(EstagioJuvenilModel.codigo_estagio == codigo_estagio.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[EstagioJuvenil]:
        stmt = select(EstagioJuvenilModel).order_by(EstagioJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[EstagioJuvenil]:
        stmt = select(EstagioJuvenilModel).where(EstagioJuvenilModel.jovem_id == jovem_id).order_by(EstagioJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusEstagio) -> list[EstagioJuvenil]:
        stmt = select(EstagioJuvenilModel).where(EstagioJuvenilModel.status == status.value).order_by(EstagioJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, estagio_id: UUID) -> bool:
        model = await self.session.get(EstagioJuvenilModel, estagio_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(EstagioJuvenilModel).where(EstagioJuvenilModel.codigo_estagio.like(f'EST/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'EST/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: EstagioJuvenilModel) -> EstagioJuvenil:
        return EstagioJuvenil(id=model.id, codigo_estagio=model.codigo_estagio, jovem_id=model.jovem_id, instituicao=model.instituicao, area_interesse=AreaInteresse(model.area_interesse), cargo=model.cargo, carga_horaria_semanal=model.carga_horaria_semanal, data_inicio=model.data_inicio, data_fim=model.data_fim, status=StatusEstagio(model.status), bolsa_auxilio=model.bolsa_auxilio, data_cadastro=model.data_cadastro, observacoes=model.observacoes, ativo=model.ativo)