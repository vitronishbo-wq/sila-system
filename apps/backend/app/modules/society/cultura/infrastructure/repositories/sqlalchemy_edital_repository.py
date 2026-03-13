from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.cultura.application.ports.edital_repository_port import EditalRepositoryPort
from apps.backend.app.modules.society.cultura.domain.enums import FaseEditalCultural, TipoEditalCultural
from apps.backend.app.modules.society.cultura.domain.models.edital import Edital
from apps.backend.app.modules.society.cultura.infrastructure.models.edital_model import EditalModel

class SQLAlchemyEditalRepository(EditalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, edital: Edital) -> Edital:
        model = await self.session.get(EditalModel, edital.id)
        if not model:
            model = EditalModel(id=edital.id)
            self.session.add(model)
        model.numero = edital.numero
        model.titulo = edital.titulo
        model.tipo = edital.tipo.value
        model.orgao_responsavel_id = edital.orgao_responsavel_id
        model.valor_total = edital.valor_total
        model.valor_disponivel = edital.valor_disponivel
        model.data_publicacao = edital.data_publicacao
        model.data_inicio_inscricoes = edital.data_inicio_inscricoes
        model.data_fim_inscricoes = edital.data_fim_inscricoes
        model.vagas = edital.vagas
        model.descricao = edital.descricao
        model.fase = edital.fase.value
        model.criterios = list(edital.criterios)
        model.documentos_necessarios = list(edital.documentos_necessarios)
        model.inscricoes = [str(item) for item in edital.inscricoes]
        model.projetos_selecionados = [str(item) for item in edital.projetos_selecionados]
        model.ativo = edital.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, edital_id: UUID) -> Edital | None:
        model = await self.session.get(EditalModel, edital_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero: str) -> Edital | None:
        stmt = select(EditalModel).where(EditalModel.numero == numero.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Edital]:
        stmt = select(EditalModel).order_by(EditalModel.data_publicacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoEditalCultural) -> list[Edital]:
        stmt = select(EditalModel).where(EditalModel.tipo == tipo.value).order_by(EditalModel.data_publicacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_fase(self, fase: FaseEditalCultural) -> list[Edital]:
        stmt = select(EditalModel).where(EditalModel.fase == fase.value).order_by(EditalModel.data_publicacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[Edital]:
        stmt = select(EditalModel).where(EditalModel.data_publicacao >= data_inicio).where(EditalModel.data_publicacao <= data_fim).order_by(EditalModel.data_publicacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def find_ativos(self) -> list[Edital]:
        stmt = select(EditalModel).where(EditalModel.ativo.is_(True)).order_by(EditalModel.data_publicacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, edital_id: UUID) -> bool:
        model = await self.session.get(EditalModel, edital_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: EditalModel) -> Edital:
        return Edital(id=model.id, numero=model.numero, titulo=model.titulo, tipo=TipoEditalCultural(model.tipo), orgao_responsavel_id=model.orgao_responsavel_id, valor_total=Decimal(model.valor_total), valor_disponivel=Decimal(model.valor_disponivel), data_publicacao=model.data_publicacao, data_inicio_inscricoes=model.data_inicio_inscricoes, data_fim_inscricoes=model.data_fim_inscricoes, vagas=model.vagas, descricao=model.descricao, fase=FaseEditalCultural(model.fase), criterios=list(model.criterios or []), documentos_necessarios=list(model.documentos_necessarios or []), inscricoes=[UUID(item) for item in model.inscricoes or []], projetos_selecionados=[UUID(item) for item in model.projetos_selecionados or []], ativo=model.ativo)