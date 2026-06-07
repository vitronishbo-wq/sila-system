from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select

from apps.backend.app.modules.resources.agricultura.application.ports import ProdutorRepositoryPort
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor
from apps.backend.app.modules.resources.agricultura.domain.models.produtor import Produtor
from apps.backend.app.modules.resources.agricultura.infrastructure.models.produtor_model import (
    ProdutorModel,
)


class SQLAlchemyProdutorRepository(ProdutorRepositoryPort):
    def __init__(self, session):
        self.session = session

    async def save(self, produtor: Produtor) -> Produtor:
        model = await self.session.get(ProdutorModel, produtor.id)
        if not model:
            model = ProdutorModel(id=produtor.id)
            self.session.add(model)
        model.cadastro_produtor = produtor.cadastro_produtor
        model.tipo = produtor.tipo.value
        model.status = produtor.status.value
        model.nome = produtor.nome
        model.documento = produtor.documento
        model.documento_tipo = produtor.documento_tipo
        model.data_cadastro = produtor.data_cadastro
        model.telefone = produtor.telefone
        model.email = produtor.email
        model.endereco = produtor.endereco
        model.citizen_id = produtor.citizen_id
        model.empresa_id = produtor.empresa_id
        model.familiar = produtor.familiar
        model.observacoes = produtor.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, produtor_id: UUID) -> Produtor | None:
        model = await self.session.get(ProdutorModel, produtor_id)
        return self._to_domain(model) if model else None

    async def get_by_cadastro(self, cadastro_produtor: str) -> Produtor | None:
        stmt = select(ProdutorModel).where(ProdutorModel.cadastro_produtor == cadastro_produtor)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_documento(self, documento: str) -> Produtor | None:
        stmt = select(ProdutorModel).where(ProdutorModel.documento == documento)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_status(self, status: StatusProdutor | None = None) -> list[Produtor]:
        stmt = select(ProdutorModel)
        if status:
            stmt = stmt.where(ProdutorModel.status == status.value)
        rows = (
            (await self.session.execute(stmt.order_by(ProdutorModel.created_at.desc())))
            .scalars()
            .all()
        )
        return [self._to_domain(item) for item in rows]

    async def next_cadastro(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(ProdutorModel)
            .where(ProdutorModel.cadastro_produtor.like(f"AGR/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"AGR/{ano}/{count + 1:06d}"

    @staticmethod
    def _to_domain(model: ProdutorModel) -> Produtor:
        return Produtor(
            id=model.id,
            cadastro_produtor=model.cadastro_produtor,
            tipo=TipoProdutor(model.tipo),
            status=StatusProdutor(model.status),
            nome=model.nome,
            documento=model.documento,
            documento_tipo=model.documento_tipo,
            data_cadastro=model.data_cadastro,
            telefone=model.telefone,
            email=model.email,
            endereco=model.endereco,
            citizen_id=model.citizen_id,
            empresa_id=model.empresa_id,
            familiar=model.familiar,
            observacoes=model.observacoes,
        )
