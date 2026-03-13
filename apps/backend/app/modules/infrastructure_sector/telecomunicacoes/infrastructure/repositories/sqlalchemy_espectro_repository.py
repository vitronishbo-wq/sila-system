from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.espectro_repository_port import EspectroRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusEspectro, TipoEspectro, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.espectro import Espectro
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.espectro_model import EspectroModel

class SQLAlchemyEspectroRepository(EspectroRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, espectro: Espectro) -> Espectro:
        model = await self.session.get(EspectroModel, espectro.id)
        if not model:
            model = EspectroModel(id=espectro.id)
            self.session.add(model)
        model.codigo_espectro = espectro.codigo_espectro
        model.tipo = espectro.tipo.value
        model.frequencia_inicial_mhz = espectro.frequencia_inicial_mhz
        model.frequencia_final_mhz = espectro.frequencia_final_mhz
        model.largura_banda_mhz = espectro.largura_banda_mhz
        model.servico_principal = espectro.servico_principal.value
        model.municipio = espectro.municipio
        model.provincia = espectro.provincia
        model.status = espectro.status.value
        model.outorga_id = espectro.outorga_id
        model.observacoes = espectro.observacoes
        model.ativo = espectro.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, espectro_id: UUID) -> Espectro | None:
        model = await self.session.get(EspectroModel, espectro_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_espectro: str) -> Espectro | None:
        stmt = select(EspectroModel).where(EspectroModel.codigo_espectro == codigo_espectro.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Espectro]:
        stmt = select(EspectroModel).order_by(EspectroModel.frequencia_inicial_mhz.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoEspectro) -> list[Espectro]:
        stmt = select(EspectroModel).where(EspectroModel.tipo == tipo.value).order_by(EspectroModel.frequencia_inicial_mhz.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Espectro]:
        normalized = municipio.strip().lower()
        stmt = select(EspectroModel).where(func.lower(EspectroModel.municipio) == normalized).order_by(EspectroModel.frequencia_inicial_mhz.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusEspectro) -> list[Espectro]:
        stmt = select(EspectroModel).where(EspectroModel.status == status.value).order_by(EspectroModel.frequencia_inicial_mhz.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, espectro_id: UUID) -> bool:
        model = await self.session.get(EspectroModel, espectro_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(EspectroModel).where(EspectroModel.codigo_espectro.like(f'ESP/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'ESP/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: EspectroModel) -> Espectro:
        return Espectro(id=model.id, codigo_espectro=model.codigo_espectro, tipo=TipoEspectro(model.tipo), frequencia_inicial_mhz=float(model.frequencia_inicial_mhz), frequencia_final_mhz=float(model.frequencia_final_mhz), largura_banda_mhz=float(model.largura_banda_mhz), servico_principal=TipoServico(model.servico_principal), municipio=model.municipio, provincia=model.provincia, status=StatusEspectro(model.status), outorga_id=model.outorga_id, observacoes=model.observacoes, ativo=model.ativo)