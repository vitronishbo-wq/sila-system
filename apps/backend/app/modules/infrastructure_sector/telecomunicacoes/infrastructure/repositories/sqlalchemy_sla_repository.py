from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.sla_repository_port import SLARepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusSLA, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.sla import SLA
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.sla_model import SLAModel

class SQLAlchemySLARepository(SLARepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, sla: SLA) -> SLA:
        model = await self.session.get(SLAModel, sla.id)
        if not model:
            model = SLAModel(id=sla.id)
            self.session.add(model)
        model.codigo_sla = sla.codigo_sla
        model.operadora_id = sla.operadora_id
        model.nome = sla.nome
        model.servico = sla.servico.value
        model.disponibilidade_min_percentual = sla.disponibilidade_min_percentual
        model.latencia_max_ms = sla.latencia_max_ms
        model.jitter_max_ms = sla.jitter_max_ms
        model.perda_pacotes_max_percentual = sla.perda_pacotes_max_percentual
        model.velocidade_download_min_mbps = sla.velocidade_download_min_mbps
        model.velocidade_upload_min_mbps = sla.velocidade_upload_min_mbps
        model.data_inicio = sla.data_inicio
        model.data_fim = sla.data_fim
        model.status = sla.status.value
        model.observacoes = sla.observacoes
        model.ativo = sla.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, sla_id: UUID) -> SLA | None:
        model = await self.session.get(SLAModel, sla_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_sla: str) -> SLA | None:
        stmt = select(SLAModel).where(SLAModel.codigo_sla == codigo_sla.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def find_ativo_por_operadora_servico(self, operadora_id: UUID, servico: TipoServico) -> SLA | None:
        stmt = select(SLAModel).where(SLAModel.operadora_id == operadora_id, SLAModel.servico == servico.value, SLAModel.status == StatusSLA.ATIVO.value, SLAModel.ativo.is_(True)).order_by(SLAModel.data_inicio.desc()).limit(1)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[SLA]:
        stmt = select(SLAModel).order_by(SLAModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora(self, operadora_id: UUID) -> list[SLA]:
        stmt = select(SLAModel).where(SLAModel.operadora_id == operadora_id).order_by(SLAModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusSLA) -> list[SLA]:
        stmt = select(SLAModel).where(SLAModel.status == status.value).order_by(SLAModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, sla_id: UUID) -> bool:
        model = await self.session.get(SLAModel, sla_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(SLAModel).where(SLAModel.codigo_sla.like(f'SLA/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'SLA/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: SLAModel) -> SLA:
        return SLA(id=model.id, codigo_sla=model.codigo_sla, operadora_id=model.operadora_id, nome=model.nome, servico=TipoServico(model.servico), disponibilidade_min_percentual=float(model.disponibilidade_min_percentual), latencia_max_ms=float(model.latencia_max_ms), jitter_max_ms=float(model.jitter_max_ms), perda_pacotes_max_percentual=float(model.perda_pacotes_max_percentual), velocidade_download_min_mbps=float(model.velocidade_download_min_mbps), velocidade_upload_min_mbps=float(model.velocidade_upload_min_mbps), data_inicio=model.data_inicio, data_fim=model.data_fim, status=StatusSLA(model.status), observacoes=model.observacoes, ativo=model.ativo)