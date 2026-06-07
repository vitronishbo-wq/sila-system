from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.juventude.application.ports.formacao_repository_port import (
    FormacaoRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusFormacao
from apps.backend.app.modules.society.juventude.domain.models.formacao_juvenil import (
    FormacaoJuvenil,
)
from apps.backend.app.modules.society.juventude.infrastructure.models.formacao_juvenil_model import (
    FormacaoJuvenilModel,
)


class SQLAlchemyFormacaoRepository(FormacaoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, formacao: FormacaoJuvenil) -> FormacaoJuvenil:
        model = await self.session.get(FormacaoJuvenilModel, formacao.id)
        if not model:
            model = FormacaoJuvenilModel(id=formacao.id)
            self.session.add(model)
        model.codigo_formacao = formacao.codigo_formacao
        model.jovem_id = formacao.jovem_id
        model.programa_id = formacao.programa_id
        model.nome_curso = formacao.nome_curso
        model.instituicao = formacao.instituicao
        model.carga_horaria = formacao.carga_horaria
        model.data_inicio = formacao.data_inicio
        model.data_fim = formacao.data_fim
        model.certificado_emitido = formacao.certificado_emitido
        model.status = formacao.status.value
        model.data_cadastro = formacao.data_cadastro
        model.observacoes = formacao.observacoes
        model.ativo = formacao.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, formacao_id: UUID) -> FormacaoJuvenil | None:
        model = await self.session.get(FormacaoJuvenilModel, formacao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_formacao: str) -> FormacaoJuvenil | None:
        stmt = select(FormacaoJuvenilModel).where(
            FormacaoJuvenilModel.codigo_formacao == codigo_formacao.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[FormacaoJuvenil]:
        stmt = select(FormacaoJuvenilModel).order_by(FormacaoJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[FormacaoJuvenil]:
        stmt = (
            select(FormacaoJuvenilModel)
            .where(FormacaoJuvenilModel.jovem_id == jovem_id)
            .order_by(FormacaoJuvenilModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_programa(self, programa_id: UUID) -> list[FormacaoJuvenil]:
        stmt = (
            select(FormacaoJuvenilModel)
            .where(FormacaoJuvenilModel.programa_id == programa_id)
            .order_by(FormacaoJuvenilModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusFormacao) -> list[FormacaoJuvenil]:
        stmt = (
            select(FormacaoJuvenilModel)
            .where(FormacaoJuvenilModel.status == status.value)
            .order_by(FormacaoJuvenilModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, formacao_id: UUID) -> bool:
        model = await self.session.get(FormacaoJuvenilModel, formacao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(FormacaoJuvenilModel)
            .where(FormacaoJuvenilModel.codigo_formacao.like(f"FRM/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"FRM/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: FormacaoJuvenilModel) -> FormacaoJuvenil:
        return FormacaoJuvenil(
            id=model.id,
            codigo_formacao=model.codigo_formacao,
            jovem_id=model.jovem_id,
            programa_id=model.programa_id,
            nome_curso=model.nome_curso,
            instituicao=model.instituicao,
            carga_horaria=model.carga_horaria,
            data_inicio=model.data_inicio,
            data_fim=model.data_fim,
            certificado_emitido=model.certificado_emitido,
            status=StatusFormacao(model.status),
            data_cadastro=model.data_cadastro,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
