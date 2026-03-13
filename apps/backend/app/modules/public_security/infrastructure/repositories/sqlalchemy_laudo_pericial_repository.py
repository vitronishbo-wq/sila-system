from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.public_security.application.ports.laudo_pericial_repository_port import LaudoPericialRepositoryPort
from apps.backend.app.modules.public_security.domain.enums import StatusLaudo, TipoLaudo
from apps.backend.app.modules.public_security.domain.models.laudo_pericial import LaudoPericial
from apps.backend.app.modules.public_security.infrastructure.models.laudo_pericial_model import LaudoPericialModel

class SQLAlchemyLaudoPericialRepository(LaudoPericialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, laudo: LaudoPericial) -> LaudoPericial:
        model = await self.session.get(LaudoPericialModel, laudo.id)
        if not model:
            model = LaudoPericialModel(id=laudo.id)
            self.session.add(model)
        model.numero_laudo = laudo.numero_laudo
        model.prova_id = laudo.prova_id
        model.tipo_laudo = laudo.tipo_laudo.value
        model.perito_id = laudo.perito_id
        model.data_emissao = laudo.data_emissao
        model.conclusao = laudo.conclusao
        model.status = laudo.status.value
        model.resumo = laudo.resumo
        model.arquivo_url = laudo.arquivo_url
        model.observacoes = laudo.observacoes
        model.ativo = laudo.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, laudo_id: UUID) -> LaudoPericial | None:
        model = await self.session.get(LaudoPericialModel, laudo_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_laudo: str) -> LaudoPericial | None:
        stmt = select(LaudoPericialModel).where(LaudoPericialModel.numero_laudo == numero_laudo.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[LaudoPericial]:
        stmt = select(LaudoPericialModel).order_by(LaudoPericialModel.data_emissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_prova(self, prova_id: UUID) -> list[LaudoPericial]:
        stmt = select(LaudoPericialModel).where(LaudoPericialModel.prova_id == prova_id).order_by(LaudoPericialModel.data_emissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoLaudo) -> list[LaudoPericial]:
        stmt = select(LaudoPericialModel).where(LaudoPericialModel.tipo_laudo == tipo.value).order_by(LaudoPericialModel.data_emissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusLaudo) -> list[LaudoPericial]:
        stmt = select(LaudoPericialModel).where(LaudoPericialModel.status == status.value).order_by(LaudoPericialModel.data_emissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, laudo_id: UUID) -> bool:
        model = await self.session.get(LaudoPericialModel, laudo_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_numero(self) -> str:
        year = date.today().year
        prefix = f'LDP/{year}/'
        stmt = select(func.count()).select_from(LaudoPericialModel).where(LaudoPericialModel.numero_laudo.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: LaudoPericialModel) -> LaudoPericial:
        return LaudoPericial(id=model.id, numero_laudo=model.numero_laudo, prova_id=model.prova_id, tipo_laudo=TipoLaudo(model.tipo_laudo), perito_id=model.perito_id, data_emissao=model.data_emissao, conclusao=model.conclusao, status=StatusLaudo(model.status), resumo=model.resumo, arquivo_url=model.arquivo_url, observacoes=model.observacoes, ativo=model.ativo)