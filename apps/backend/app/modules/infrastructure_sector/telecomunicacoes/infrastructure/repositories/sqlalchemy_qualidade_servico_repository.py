from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.qualidade_servico_repository_port import (
    QualidadeServicoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusQualidadeServico,
    TipoServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.qualidade_servico import (
    QualidadeServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.qualidade_servico_model import (
    QualidadeServicoModel,
)


class SQLAlchemyQualidadeServicoRepository(QualidadeServicoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, medicao: QualidadeServico) -> QualidadeServico:
        model = await self.session.get(QualidadeServicoModel, medicao.id)
        if not model:
            model = QualidadeServicoModel(id=medicao.id)
            self.session.add(model)
        model.codigo_medicao = medicao.codigo_medicao
        model.operadora_id = medicao.operadora_id
        model.assinante_id = medicao.assinante_id
        model.sla_id = medicao.sla_id
        model.servico = medicao.servico.value
        model.data_medicao = medicao.data_medicao
        model.disponibilidade_percentual = medicao.disponibilidade_percentual
        model.latencia_ms = medicao.latencia_ms
        model.jitter_ms = medicao.jitter_ms
        model.perda_pacotes_percentual = medicao.perda_pacotes_percentual
        model.velocidade_download_mbps = medicao.velocidade_download_mbps
        model.velocidade_upload_mbps = medicao.velocidade_upload_mbps
        model.status = medicao.status.value
        model.observacoes = medicao.observacoes
        model.ativo = medicao.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, medicao_id: UUID) -> QualidadeServico | None:
        model = await self.session.get(QualidadeServicoModel, medicao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_medicao: str) -> QualidadeServico | None:
        stmt = select(QualidadeServicoModel).where(
            QualidadeServicoModel.codigo_medicao == codigo_medicao.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[QualidadeServico]:
        stmt = select(QualidadeServicoModel).order_by(QualidadeServicoModel.data_medicao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora(self, operadora_id: UUID) -> list[QualidadeServico]:
        stmt = (
            select(QualidadeServicoModel)
            .where(QualidadeServicoModel.operadora_id == operadora_id)
            .order_by(QualidadeServicoModel.data_medicao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora_periodo(
        self, operadora_id: UUID, referencia_ano: int, referencia_mes: int
    ) -> list[QualidadeServico]:
        start = date(referencia_ano, referencia_mes, 1)
        if referencia_mes == 12:
            end = date(referencia_ano + 1, 1, 1)
        else:
            end = date(referencia_ano, referencia_mes + 1, 1)
        stmt = (
            select(QualidadeServicoModel)
            .where(
                QualidadeServicoModel.operadora_id == operadora_id,
                QualidadeServicoModel.data_medicao >= start,
                QualidadeServicoModel.data_medicao < end,
            )
            .order_by(QualidadeServicoModel.data_medicao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_assinante(self, assinante_id: UUID) -> list[QualidadeServico]:
        stmt = (
            select(QualidadeServicoModel)
            .where(QualidadeServicoModel.assinante_id == assinante_id)
            .order_by(QualidadeServicoModel.data_medicao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusQualidadeServico) -> list[QualidadeServico]:
        stmt = (
            select(QualidadeServicoModel)
            .where(QualidadeServicoModel.status == status.value)
            .order_by(QualidadeServicoModel.data_medicao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, medicao_id: UUID) -> bool:
        model = await self.session.get(QualidadeServicoModel, medicao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(QualidadeServicoModel)
            .where(QualidadeServicoModel.codigo_medicao.like(f"QLT/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"QLT/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: QualidadeServicoModel) -> QualidadeServico:
        return QualidadeServico(
            id=model.id,
            codigo_medicao=model.codigo_medicao,
            operadora_id=model.operadora_id,
            assinante_id=model.assinante_id,
            sla_id=model.sla_id,
            servico=TipoServico(model.servico),
            data_medicao=model.data_medicao,
            disponibilidade_percentual=float(model.disponibilidade_percentual),
            latencia_ms=float(model.latencia_ms),
            jitter_ms=float(model.jitter_ms),
            perda_pacotes_percentual=float(model.perda_pacotes_percentual),
            velocidade_download_mbps=float(model.velocidade_download_mbps),
            velocidade_upload_mbps=float(model.velocidade_upload_mbps),
            status=StatusQualidadeServico(model.status),
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
