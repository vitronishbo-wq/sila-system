from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.juventude.application.ports.mentor_repository_port import (
    MentorRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusMentoria,
    TipoMentoria,
)
from apps.backend.app.modules.society.juventude.domain.models.mentor import Mentor
from apps.backend.app.modules.society.juventude.infrastructure.models.mentor_model import (
    MentorModel,
)


class SQLAlchemyMentorRepository(MentorRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, mentor: Mentor) -> Mentor:
        model = await self.session.get(MentorModel, mentor.id)
        if not model:
            model = MentorModel(id=mentor.id)
            self.session.add(model)
        model.codigo_mentor = mentor.codigo_mentor
        model.nome = mentor.nome
        model.tipo_mentoria = mentor.tipo_mentoria.value
        model.area_interesse = mentor.area_interesse.value
        model.email = mentor.email
        model.telefone = mentor.telefone
        model.jovem_ids = mentor.jovem_ids
        model.status = mentor.status.value
        model.data_cadastro = mentor.data_cadastro
        model.observacoes = mentor.observacoes
        model.ativo = mentor.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, mentor_id: UUID) -> Mentor | None:
        model = await self.session.get(MentorModel, mentor_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_mentor: str) -> Mentor | None:
        stmt = select(MentorModel).where(MentorModel.codigo_mentor == codigo_mentor.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Mentor]:
        stmt = select(MentorModel).order_by(MentorModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusMentoria) -> list[Mentor]:
        stmt = (
            select(MentorModel)
            .where(MentorModel.status == status.value)
            .order_by(MentorModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, mentor_id: UUID) -> bool:
        model = await self.session.get(MentorModel, mentor_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(MentorModel)
            .where(MentorModel.codigo_mentor.like(f"MEN/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"MEN/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: MentorModel) -> Mentor:
        return Mentor(
            id=model.id,
            codigo_mentor=model.codigo_mentor,
            nome=model.nome,
            tipo_mentoria=TipoMentoria(model.tipo_mentoria),
            area_interesse=AreaInteresse(model.area_interesse),
            email=model.email,
            telefone=model.telefone,
            jovem_ids=model.jovem_ids,
            status=StatusMentoria(model.status),
            data_cadastro=model.data_cadastro or date.today(),
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
