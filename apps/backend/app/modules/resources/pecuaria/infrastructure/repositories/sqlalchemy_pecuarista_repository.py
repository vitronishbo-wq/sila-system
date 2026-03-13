from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pecuaria.application.ports import PecuaristaRepositoryPort
from apps.backend.app.modules.resources.pecuaria.domain.enums import StatusPecuarista
from apps.backend.app.modules.resources.pecuaria.domain.models.pecuarista import Pecuarista
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.pecuarista_model import PecuaristaModel

class SQLAlchemyPecuaristaRepository(PecuaristaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, item: Pecuarista) -> Pecuarista:
        model = await self.session.get(PecuaristaModel, item.id)
        if not model:
            model = PecuaristaModel(id=item.id)
            self.session.add(model)
        model.cadastro_pecuarista = item.cadastro_pecuarista
        model.nome = item.nome
        model.documento = item.documento
        model.documento_tipo = item.documento_tipo
        model.data_cadastro = item.data_cadastro
        model.status = item.status.value
        model.telefone = item.telefone
        model.email = item.email
        model.endereco = item.endereco
        model.citizen_id = item.citizen_id
        model.empresa_id = item.empresa_id
        model.observacoes = item.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, pecuarista_id: UUID) -> Pecuarista | None:
        model = await self.session.get(PecuaristaModel, pecuarista_id)
        return self._to_domain(model) if model else None

    async def get_by_cadastro(self, cadastro_pecuarista: str) -> Pecuarista | None:
        stmt = select(PecuaristaModel).where(PecuaristaModel.cadastro_pecuarista == cadastro_pecuarista)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_documento(self, documento: str) -> Pecuarista | None:
        stmt = select(PecuaristaModel).where(PecuaristaModel.documento == documento)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_status(self, status: StatusPecuarista | None=None) -> list[Pecuarista]:
        stmt = select(PecuaristaModel)
        if status:
            stmt = stmt.where(PecuaristaModel.status == status.value)
        rows = (await self.session.execute(stmt.order_by(PecuaristaModel.created_at.desc()))).scalars().all()
        return [self._to_domain(model) for model in rows]

    async def next_cadastro(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(PecuaristaModel).where(PecuaristaModel.cadastro_pecuarista.like(f'PEC/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PEC/{ano}/{count + 1:06d}'

    @staticmethod
    def _to_domain(model: PecuaristaModel) -> Pecuarista:
        return Pecuarista(id=model.id, cadastro_pecuarista=model.cadastro_pecuarista, nome=model.nome, documento=model.documento, documento_tipo=model.documento_tipo, data_cadastro=model.data_cadastro, status=StatusPecuarista(model.status), telefone=model.telefone, email=model.email, endereco=model.endereco, citizen_id=model.citizen_id, empresa_id=model.empresa_id, observacoes=model.observacoes)