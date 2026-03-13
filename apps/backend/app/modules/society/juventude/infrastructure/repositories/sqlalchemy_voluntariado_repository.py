from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.juventude.application.ports.voluntariado_repository_port import VoluntariadoRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusVoluntariado
from apps.backend.app.modules.society.juventude.domain.models.voluntariado import Voluntariado
from apps.backend.app.modules.society.juventude.infrastructure.models.voluntariado_model import VoluntariadoModel

class SQLAlchemyVoluntariadoRepository(VoluntariadoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, voluntariado: Voluntariado) -> Voluntariado:
        model = await self.session.get(VoluntariadoModel, voluntariado.id)
        if not model:
            model = VoluntariadoModel(id=voluntariado.id)
            self.session.add(model)
        model.codigo_voluntariado = voluntariado.codigo_voluntariado
        model.jovem_id = voluntariado.jovem_id
        model.organizacao = voluntariado.organizacao
        model.causa = voluntariado.causa.value
        model.carga_horaria_total = voluntariado.carga_horaria_total
        model.data_inicio = voluntariado.data_inicio
        model.data_fim = voluntariado.data_fim
        model.status = voluntariado.status.value
        model.data_cadastro = voluntariado.data_cadastro
        model.observacoes = voluntariado.observacoes
        model.ativo = voluntariado.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, voluntariado_id: UUID) -> Voluntariado | None:
        model = await self.session.get(VoluntariadoModel, voluntariado_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_voluntariado: str) -> Voluntariado | None:
        stmt = select(VoluntariadoModel).where(VoluntariadoModel.codigo_voluntariado == codigo_voluntariado.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Voluntariado]:
        stmt = select(VoluntariadoModel).order_by(VoluntariadoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[Voluntariado]:
        stmt = select(VoluntariadoModel).where(VoluntariadoModel.jovem_id == jovem_id).order_by(VoluntariadoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusVoluntariado) -> list[Voluntariado]:
        stmt = select(VoluntariadoModel).where(VoluntariadoModel.status == status.value).order_by(VoluntariadoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, voluntariado_id: UUID) -> bool:
        model = await self.session.get(VoluntariadoModel, voluntariado_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(VoluntariadoModel).where(VoluntariadoModel.codigo_voluntariado.like(f'VOL/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'VOL/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: VoluntariadoModel) -> Voluntariado:
        return Voluntariado(id=model.id, codigo_voluntariado=model.codigo_voluntariado, jovem_id=model.jovem_id, organizacao=model.organizacao, causa=AreaInteresse(model.causa), carga_horaria_total=model.carga_horaria_total, data_inicio=model.data_inicio, data_fim=model.data_fim, status=StatusVoluntariado(model.status), data_cadastro=model.data_cadastro or date.today(), observacoes=model.observacoes, ativo=model.ativo)