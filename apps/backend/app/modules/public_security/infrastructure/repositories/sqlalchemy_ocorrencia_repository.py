from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.public_security.application.ports.ocorrencia_repository_port import OcorrenciaRepositoryPort
from app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusOcorrencia, TipoOcorrencia
from app.modules.public_security.domain.models.ocorrencia import Ocorrencia
from app.modules.public_security.infrastructure.models.ocorrencia_model import OcorrenciaModel

class SQLAlchemyOcorrenciaRepository(OcorrenciaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        model = await self.session.get(OcorrenciaModel, ocorrencia.id)
        if not model:
            model = OcorrenciaModel(id=ocorrencia.id)
            self.session.add(model)
        model.codigo_ocorrencia = ocorrencia.codigo_ocorrencia
        model.unidade_id = ocorrencia.unidade_id
        model.policial_responsavel_id = ocorrencia.policial_responsavel_id
        model.tipo = ocorrencia.tipo.value
        model.status = ocorrencia.status.value
        model.prioridade = ocorrencia.prioridade.value
        model.data_ocorrencia = ocorrencia.data_ocorrencia
        model.descricao = ocorrencia.descricao
        model.municipio = ocorrencia.municipio
        model.provincia = ocorrencia.provincia
        model.endereco = ocorrencia.endereco
        model.vitimas = ocorrencia.vitimas
        model.suspeitos = ocorrencia.suspeitos
        model.preso_em_flagrante = ocorrencia.preso_em_flagrante
        model.data_registro = ocorrencia.data_registro
        model.observacoes = ocorrencia.observacoes
        model.ativo = ocorrencia.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, ocorrencia_id: UUID) -> Ocorrencia | None:
        model = await self.session.get(OcorrenciaModel, ocorrencia_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_ocorrencia: str) -> Ocorrencia | None:
        stmt = select(OcorrenciaModel).where(OcorrenciaModel.codigo_ocorrencia == codigo_ocorrencia.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Ocorrencia]:
        stmt = select(OcorrenciaModel).order_by(OcorrenciaModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_unidade(self, unidade_id: UUID) -> list[Ocorrencia]:
        stmt = select(OcorrenciaModel).where(OcorrenciaModel.unidade_id == unidade_id).order_by(OcorrenciaModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoOcorrencia) -> list[Ocorrencia]:
        stmt = select(OcorrenciaModel).where(OcorrenciaModel.tipo == tipo.value).order_by(OcorrenciaModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusOcorrencia) -> list[Ocorrencia]:
        stmt = select(OcorrenciaModel).where(OcorrenciaModel.status == status.value).order_by(OcorrenciaModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[Ocorrencia]:
        stmt = select(OcorrenciaModel).where(OcorrenciaModel.data_ocorrencia >= inicio, OcorrenciaModel.data_ocorrencia <= fim).order_by(OcorrenciaModel.data_ocorrencia.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, ocorrencia_id: UUID) -> bool:
        model = await self.session.get(OcorrenciaModel, ocorrencia_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'OCO/{year}/'
        stmt = select(func.count()).select_from(OcorrenciaModel).where(OcorrenciaModel.codigo_ocorrencia.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: OcorrenciaModel) -> Ocorrencia:
        return Ocorrencia(id=model.id, codigo_ocorrencia=model.codigo_ocorrencia, unidade_id=model.unidade_id, policial_responsavel_id=model.policial_responsavel_id, tipo=TipoOcorrencia(model.tipo), status=StatusOcorrencia(model.status), prioridade=PrioridadeOcorrencia(model.prioridade), data_ocorrencia=model.data_ocorrencia, descricao=model.descricao, municipio=model.municipio, provincia=model.provincia, endereco=model.endereco, vitimas=model.vitimas, suspeitos=model.suspeitos, preso_em_flagrante=model.preso_em_flagrante, data_registro=model.data_registro, observacoes=model.observacoes, ativo=model.ativo)