from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.civil_protection.domain.ports.atendimento_repository_port import AtendimentoRepositoryPort
from apps.backend.app.modules.civil_protection.domain.enums import StatusAtendimento
from apps.backend.app.modules.civil_protection.domain.models.atendimento import Atendimento
from apps.backend.app.modules.civil_protection.infrastructure.models.atendimento_model import AtendimentoModel

class SQLAlchemyAtendimentoRepository(AtendimentoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, atendimento: Atendimento) -> Atendimento:
        model = await self.session.get(AtendimentoModel, atendimento.id)
        if not model:
            model = AtendimentoModel(id=atendimento.id)
            self.session.add(model)
        model.codigo_atendimento = atendimento.codigo_atendimento
        model.despacho_id = atendimento.despacho_id
        model.ocorrencia_id = atendimento.ocorrencia_id
        model.status = atendimento.status.value
        model.inicio_atendimento = atendimento.inicio_atendimento
        model.fim_atendimento = atendimento.fim_atendimento
        model.local_atendimento = atendimento.local_atendimento
        model.resumo = atendimento.resumo
        model.vitimas_atendidas = atendimento.vitimas_atendidas
        model.desalojados_atendidos = atendimento.desalojados_atendidos
        model.obitos_confirmados = atendimento.obitos_confirmados
        model.equipe_responsavel_id = atendimento.equipe_responsavel_id
        model.observacoes = atendimento.observacoes
        model.ativo = atendimento.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, atendimento_id: UUID) -> Atendimento | None:
        model = await self.session.get(AtendimentoModel, atendimento_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_atendimento: str) -> Atendimento | None:
        stmt = select(AtendimentoModel).where(AtendimentoModel.codigo_atendimento == codigo_atendimento.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Atendimento]:
        stmt = select(AtendimentoModel).order_by(AtendimentoModel.inicio_atendimento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Atendimento]:
        stmt = select(AtendimentoModel).where(AtendimentoModel.ocorrencia_id == ocorrencia_id).order_by(AtendimentoModel.inicio_atendimento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_despacho(self, despacho_id: UUID) -> list[Atendimento]:
        stmt = select(AtendimentoModel).where(AtendimentoModel.despacho_id == despacho_id).order_by(AtendimentoModel.inicio_atendimento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusAtendimento) -> list[Atendimento]:
        stmt = select(AtendimentoModel).where(AtendimentoModel.status == status.value).order_by(AtendimentoModel.inicio_atendimento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, atendimento_id: UUID) -> bool:
        model = await self.session.get(AtendimentoModel, atendimento_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'ATE/{year}/'
        stmt = select(func.count()).select_from(AtendimentoModel).where(AtendimentoModel.codigo_atendimento.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: AtendimentoModel) -> Atendimento:
        return Atendimento(id=model.id, codigo_atendimento=model.codigo_atendimento, despacho_id=model.despacho_id, ocorrencia_id=model.ocorrencia_id, status=StatusAtendimento(model.status), inicio_atendimento=model.inicio_atendimento, fim_atendimento=model.fim_atendimento, local_atendimento=model.local_atendimento, resumo=model.resumo, vitimas_atendidas=model.vitimas_atendidas, desalojados_atendidos=model.desalojados_atendidos, obitos_confirmados=model.obitos_confirmados, equipe_responsavel_id=model.equipe_responsavel_id, observacoes=model.observacoes, ativo=model.ativo)