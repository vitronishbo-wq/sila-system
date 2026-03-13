from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.cultura.application.ports.projeto_cultural_repository_port import ProjetoCulturalRepositoryPort
from app.modules.society.cultura.domain.enums import NaturezaProjetoCultural, StatusProjetoCultural, TipoProjetoCultural
from app.modules.society.cultura.domain.models.projeto_cultural import ProjetoCultural
from app.modules.society.cultura.infrastructure.models.projeto_cultural_model import ProjetoCulturalModel

class SQLAlchemyProjetoCulturalRepository(ProjetoCulturalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, projeto: ProjetoCultural) -> ProjetoCultural:
        model = await self.session.get(ProjetoCulturalModel, projeto.id)
        if not model:
            model = ProjetoCulturalModel(id=projeto.id)
            self.session.add(model)
        model.codigo_projeto = projeto.codigo_projeto
        model.titulo = projeto.titulo
        model.tipo = projeto.tipo.value
        model.natureza = projeto.natureza.value
        model.proponente_cpf_cnpj = projeto.proponente_cpf_cnpj
        model.proponente_nome = projeto.proponente_nome
        model.resumo = projeto.resumo
        model.valor_solicitado = projeto.valor_solicitado
        model.valor_aprovado = projeto.valor_aprovado
        model.data_submissao = projeto.data_submissao
        model.data_inicio = projeto.data_inicio
        model.data_fim = projeto.data_fim
        model.status = projeto.status.value
        model.edital_id = projeto.edital_id
        model.justificativa = projeto.justificativa
        model.objetivos = list(projeto.objetivos)
        model.ativo = projeto.ativo
        model.observacoes = projeto.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, projeto_id: UUID) -> ProjetoCultural | None:
        model = await self.session.get(ProjetoCulturalModel, projeto_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoCultural | None:
        stmt = select(ProjetoCulturalModel).where(ProjetoCulturalModel.codigo_projeto == codigo_projeto.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[ProjetoCultural]:
        stmt = select(ProjetoCulturalModel).order_by(ProjetoCulturalModel.data_submissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoProjetoCultural) -> list[ProjetoCultural]:
        stmt = select(ProjetoCulturalModel).where(ProjetoCulturalModel.tipo == tipo.value).order_by(ProjetoCulturalModel.data_submissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusProjetoCultural) -> list[ProjetoCultural]:
        stmt = select(ProjetoCulturalModel).where(ProjetoCulturalModel.status == status.value).order_by(ProjetoCulturalModel.data_submissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[ProjetoCultural]:
        stmt = select(ProjetoCulturalModel).where(ProjetoCulturalModel.data_submissao >= data_inicio).where(ProjetoCulturalModel.data_submissao <= data_fim).order_by(ProjetoCulturalModel.data_submissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, projeto_id: UUID) -> bool:
        model = await self.session.get(ProjetoCulturalModel, projeto_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(ProjetoCulturalModel).where(ProjetoCulturalModel.codigo_projeto.like(f'PROJ/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PROJ/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ProjetoCulturalModel) -> ProjetoCultural:
        return ProjetoCultural(id=model.id, codigo_projeto=model.codigo_projeto, titulo=model.titulo, tipo=TipoProjetoCultural(model.tipo), natureza=NaturezaProjetoCultural(model.natureza), proponente_cpf_cnpj=model.proponente_cpf_cnpj, proponente_nome=model.proponente_nome, resumo=model.resumo, valor_solicitado=Decimal(model.valor_solicitado), data_submissao=model.data_submissao, status=StatusProjetoCultural(model.status), justificativa=model.justificativa, edital_id=model.edital_id, valor_aprovado=Decimal(model.valor_aprovado) if model.valor_aprovado is not None else None, data_inicio=model.data_inicio, data_fim=model.data_fim, ativo=model.ativo, objetivos=list(model.objetivos or []), observacoes=model.observacoes)