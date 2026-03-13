from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pescas.application.ports import LicencaPescaRepositoryPort
from apps.backend.app.modules.resources.pescas.domain.enums import StatusLicenca
from apps.backend.app.modules.resources.pescas.domain.models.licenca_pesca import LicencaPesca
from apps.backend.app.modules.resources.pescas.infrastructure.models.licenca_pesca_model import LicencaPescaModel

class SQLAlchemyLicencaPescaRepository(LicencaPescaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, licenca: LicencaPesca) -> LicencaPesca:
        model = await self.session.get(LicencaPescaModel, licenca.id)
        if not model:
            model = LicencaPescaModel(id=licenca.id)
            self.session.add(model)
        model.numero_licenca = licenca.numero_licenca
        model.embarcacao_id = licenca.embarcacao_id
        model.titular_id = licenca.titular_id
        model.data_emissao = licenca.data_emissao
        model.data_validade = licenca.data_validade
        model.status = licenca.status.value
        model.modalidade_autorizada = licenca.modalidade_autorizada
        model.zona_pesca_id = licenca.zona_pesca_id
        model.observacoes = licenca.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, licenca_id: UUID) -> LicencaPesca | None:
        model = await self.session.get(LicencaPescaModel, licenca_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_licenca: str) -> LicencaPesca | None:
        stmt = select(LicencaPescaModel).where(LicencaPescaModel.numero_licenca == numero_licenca)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_embarcacao(self, embarcacao_id: UUID) -> list[LicencaPesca]:
        stmt = select(LicencaPescaModel).where(LicencaPescaModel.embarcacao_id == embarcacao_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_validas(self, referencia: date) -> list[LicencaPesca]:
        stmt = select(LicencaPescaModel).where(LicencaPescaModel.data_validade >= referencia)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_numero(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(LicencaPescaModel).where(LicencaPescaModel.numero_licenca.like(f'LIC/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'LIC/{ano}/{count + 1:06d}'

    @staticmethod
    def _to_domain(model: LicencaPescaModel) -> LicencaPesca:
        return LicencaPesca(id=model.id, numero_licenca=model.numero_licenca, embarcacao_id=model.embarcacao_id, titular_id=model.titular_id, data_emissao=model.data_emissao, data_validade=model.data_validade, status=StatusLicenca(model.status), modalidade_autorizada=model.modalidade_autorizada, zona_pesca_id=model.zona_pesca_id, observacoes=model.observacoes)