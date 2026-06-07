from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.proprietario_repository_port import (
    ProprietarioRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    TipoPessoa,
    TipoTitularidade,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.proprietario import (
    Proprietario,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.models.proprietario_model import (
    ProprietarioModel,
)


class SQLAlchemyProprietarioRepository(ProprietarioRepositoryPort):
    """Repository com suporte ORM real e fallback in-memory."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Proprietario] = {}
        self._doc_index: dict[str, str] = {}
        self._seq = 0

    async def save(self, item: Proprietario) -> Proprietario:
        if self._session:
            existing = await self._session.execute(
                select(ProprietarioModel).where(
                    ProprietarioModel.numero_cadastro == item.numero_cadastro
                )
            )
            model = existing.scalars().first()
            if model is None:
                model = ProprietarioModel(
                    id=item.id,
                    numero_cadastro=item.numero_cadastro,
                    nome=item.nome,
                    documento=item.documento,
                    tipo_pessoa=item.tipo_pessoa.value,
                    tipo_titularidade=item.tipo_titularidade.value,
                    data_cadastro=item.data_cadastro,
                    ativo=item.ativo,
                    percentual_titularidade=item.percentual_titularidade,
                    email=item.email,
                    telefone=item.telefone,
                    endereco=item.endereco,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                )
                self._session.add(model)
            else:
                model.nome = item.nome
                model.documento = item.documento
                model.tipo_pessoa = item.tipo_pessoa.value
                model.tipo_titularidade = item.tipo_titularidade.value
                model.ativo = item.ativo
                model.percentual_titularidade = item.percentual_titularidade
                model.email = item.email
                model.telefone = item.telefone
                model.endereco = item.endereco
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.numero_cadastro] = item
        self._doc_index[item.documento] = item.numero_cadastro
        return item

    async def get_by_numero_cadastro(self, numero_cadastro: str) -> Proprietario | None:
        if self._session:
            result = await self._session.execute(
                select(ProprietarioModel).where(
                    ProprietarioModel.numero_cadastro == numero_cadastro
                )
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(numero_cadastro)

    async def get_by_documento(self, documento: str) -> Proprietario | None:
        if self._session:
            result = await self._session.execute(
                select(ProprietarioModel).where(ProprietarioModel.documento == documento)
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        numero = self._doc_index.get(documento)
        if not numero:
            return None
        return self._items.get(numero)

    async def list(
        self, *, tipo_pessoa: str | None = None, ativo: bool | None = None
    ) -> list[Proprietario]:
        if self._session:
            statement = select(ProprietarioModel)
            if tipo_pessoa:
                statement = statement.where(
                    func.lower(ProprietarioModel.tipo_pessoa) == tipo_pessoa.strip().lower()
                )
            if ativo is not None:
                statement = statement.where(ProprietarioModel.ativo == ativo)
            result = await self._session.execute(
                statement.order_by(ProprietarioModel.numero_cadastro.asc())
            )
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if tipo_pessoa:
            tp = tipo_pessoa.strip().lower()
            values = [item for item in values if item.tipo_pessoa.value == tp]
        if ativo is not None:
            values = [item for item in values if item.ativo == ativo]
        return values

    async def next_numero_cadastro(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f"PRP/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(ProprietarioModel)
                .where(ProprietarioModel.numero_cadastro.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"PRP/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: ProprietarioModel) -> Proprietario:
        return Proprietario(
            id=model.id,
            numero_cadastro=model.numero_cadastro,
            nome=model.nome,
            documento=model.documento,
            tipo_pessoa=TipoPessoa(model.tipo_pessoa),
            tipo_titularidade=TipoTitularidade(model.tipo_titularidade),
            data_cadastro=model.data_cadastro,
            ativo=model.ativo,
            percentual_titularidade=Decimal(model.percentual_titularidade)
            if model.percentual_titularidade is not None
            else None,
            email=model.email,
            telefone=model.telefone,
            endereco=model.endereco,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
        )
