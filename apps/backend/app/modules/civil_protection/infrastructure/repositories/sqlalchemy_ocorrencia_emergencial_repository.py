from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.civil_protection.application.ports.ocorrencia_emergencial_repository_port import OcorrenciaEmergencialRepositoryPort
from apps.backend.app.modules.civil_protection.domain.enums import PrioridadeAtendimento, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial
from apps.backend.app.modules.civil_protection.domain.models.ocorrencia_emergencial import OcorrenciaEmergencial
from apps.backend.app.modules.civil_protection.infrastructure.models.ocorrencia_emergencial_model import OcorrenciaEmergencialModel

class SQLAlchemyOcorrenciaEmergencialRepository(OcorrenciaEmergencialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, ocorrencia: OcorrenciaEmergencial) -> OcorrenciaEmergencial:
        model = await self.session.get(OcorrenciaEmergencialModel, ocorrencia.id)
        if not model:
            model = OcorrenciaEmergencialModel(id=ocorrencia.id)
            self.session.add(model)
        model.codigo_ocorrencia = ocorrencia.codigo_ocorrencia
        model.corporacao_id = ocorrencia.corporacao_id
        model.bombeiro_responsavel_id = ocorrencia.bombeiro_responsavel_id
        model.tipo = ocorrencia.tipo.value
        model.status = ocorrencia.status.value
        model.prioridade = ocorrencia.prioridade.value
        model.data_ocorrencia = ocorrencia.data_ocorrencia
        model.descricao = ocorrencia.descricao
        model.municipio = ocorrencia.municipio
        model.provincia = ocorrencia.provincia
        model.endereco = ocorrencia.endereco
        model.vitimas = ocorrencia.vitimas
        model.desalojados = ocorrencia.desalojados
        model.obitos = ocorrencia.obitos
        model.data_registro = ocorrencia.data_registro
        model.observacoes = ocorrencia.observacoes
        model.ativo = ocorrencia.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, ocorrencia_id: UUID) -> OcorrenciaEmergencial | None:
        model = await self.session.get(OcorrenciaEmergencialModel, ocorrencia_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_ocorrencia: str) -> OcorrenciaEmergencial | None:
        stmt = select(OcorrenciaEmergencialModel).where(OcorrenciaEmergencialModel.codigo_ocorrencia == codigo_ocorrencia.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[OcorrenciaEmergencial]:
        stmt = select(OcorrenciaEmergencialModel).order_by(OcorrenciaEmergencialModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_corporacao(self, corporacao_id: UUID) -> list[OcorrenciaEmergencial]:
        stmt = select(OcorrenciaEmergencialModel).where(OcorrenciaEmergencialModel.corporacao_id == corporacao_id).order_by(OcorrenciaEmergencialModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoOcorrenciaEmergencial) -> list[OcorrenciaEmergencial]:
        stmt = select(OcorrenciaEmergencialModel).where(OcorrenciaEmergencialModel.tipo == tipo.value).order_by(OcorrenciaEmergencialModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusOcorrenciaEmergencial) -> list[OcorrenciaEmergencial]:
        stmt = select(OcorrenciaEmergencialModel).where(OcorrenciaEmergencialModel.status == status.value).order_by(OcorrenciaEmergencialModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[OcorrenciaEmergencial]:
        stmt = select(OcorrenciaEmergencialModel).where(OcorrenciaEmergencialModel.data_ocorrencia >= inicio).where(OcorrenciaEmergencialModel.data_ocorrencia <= fim).order_by(OcorrenciaEmergencialModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, ocorrencia_id: UUID) -> bool:
        model = await self.session.get(OcorrenciaEmergencialModel, ocorrencia_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'OCE/{year}/'
        stmt = select(func.count()).select_from(OcorrenciaEmergencialModel).where(OcorrenciaEmergencialModel.codigo_ocorrencia.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: OcorrenciaEmergencialModel) -> OcorrenciaEmergencial:
        return OcorrenciaEmergencial(id=model.id, codigo_ocorrencia=model.codigo_ocorrencia, corporacao_id=model.corporacao_id, tipo=TipoOcorrenciaEmergencial(model.tipo), status=StatusOcorrenciaEmergencial(model.status), prioridade=PrioridadeAtendimento(model.prioridade), data_ocorrencia=model.data_ocorrencia, descricao=model.descricao, municipio=model.municipio, provincia=model.provincia, data_registro=model.data_registro, bombeiro_responsavel_id=model.bombeiro_responsavel_id, endereco=model.endereco, vitimas=model.vitimas, desalojados=model.desalojados, obitos=model.obitos, observacoes=model.observacoes, ativo=model.ativo)