from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.outorga_espectro_repository_port import OutorgaEspectroRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOutorga
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.outorga_espectro import OutorgaEspectro
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.outorga_espectro_model import OutorgaEspectroModel

class SQLAlchemyOutorgaEspectroRepository(OutorgaEspectroRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, outorga: OutorgaEspectro) -> OutorgaEspectro:
        model = await self.session.get(OutorgaEspectroModel, outorga.id)
        if not model:
            model = OutorgaEspectroModel(id=outorga.id)
            self.session.add(model)
        model.numero_outorga = outorga.numero_outorga
        model.operadora_id = outorga.operadora_id
        model.tipo_outorga = outorga.tipo_outorga.value
        model.faixa_inicio_mhz = outorga.faixa_inicio_mhz
        model.faixa_fim_mhz = outorga.faixa_fim_mhz
        model.data_outorga = outorga.data_outorga
        model.data_validade = outorga.data_validade
        model.status = outorga.status.value
        model.observacoes = outorga.observacoes
        model.ativo = outorga.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, outorga_id: UUID) -> OutorgaEspectro | None:
        model = await self.session.get(OutorgaEspectroModel, outorga_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_outorga: str) -> OutorgaEspectro | None:
        stmt = select(OutorgaEspectroModel).where(OutorgaEspectroModel.numero_outorga == numero_outorga.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[OutorgaEspectro]:
        stmt = select(OutorgaEspectroModel).order_by(OutorgaEspectroModel.data_outorga.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora(self, operadora_id: UUID) -> list[OutorgaEspectro]:
        stmt = select(OutorgaEspectroModel).where(OutorgaEspectroModel.operadora_id == operadora_id).order_by(OutorgaEspectroModel.data_outorga.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusOutorga) -> list[OutorgaEspectro]:
        stmt = select(OutorgaEspectroModel).where(OutorgaEspectroModel.status == status.value).order_by(OutorgaEspectroModel.data_outorga.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, outorga_id: UUID) -> bool:
        model = await self.session.get(OutorgaEspectroModel, outorga_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_numero(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(OutorgaEspectroModel).where(OutorgaEspectroModel.numero_outorga.like(f'OUT/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'OUT/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: OutorgaEspectroModel) -> OutorgaEspectro:
        return OutorgaEspectro(id=model.id, numero_outorga=model.numero_outorga, operadora_id=model.operadora_id, tipo_outorga=TipoOutorga(model.tipo_outorga), faixa_inicio_mhz=float(model.faixa_inicio_mhz), faixa_fim_mhz=float(model.faixa_fim_mhz), data_outorga=model.data_outorga, data_validade=model.data_validade, status=StatusOutorga(model.status), observacoes=model.observacoes, ativo=model.ativo)