from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select

from apps.backend.app.modules.society.emprego.application.ports import CandidatoRepositoryPort
from apps.backend.app.modules.society.emprego.domain.enums import (
    Escolaridade,
    SituacaoProfissional,
    StatusCandidato,
)
from apps.backend.app.modules.society.emprego.domain.models.candidato import Candidato
from apps.backend.app.modules.society.emprego.infrastructure.models.candidato_model import (
    CandidatoModel,
)


class SQLAlchemyCandidatoRepository(CandidatoRepositoryPort):
    def __init__(self, session):
        self.session = session

    async def save(self, candidato: Candidato) -> Candidato:
        model = await self.session.get(CandidatoModel, candidato.id)
        if not model:
            model = CandidatoModel(id=candidato.id)
            self.session.add(model)
        model.numero_processo = candidato.numero_processo
        model.citizen_id = candidato.citizen_id
        model.data_registro = candidato.data_registro
        model.escolaridade = candidato.escolaridade.value
        model.situacao = candidato.situacao.value
        model.areas_interesse = candidato.areas_interesse
        model.experiencias = candidato.experiencias
        model.habilidades = candidato.habilidades
        model.status = candidato.status.value
        model.observacoes = candidato.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID):
        model = await self.session.get(CandidatoModel, id)
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID):
        stmt = select(CandidatoModel).where(CandidatoModel.citizen_id == citizen_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_filtros(
        self, escolaridade=None, situacao=None, area_interesse=None, ativos=True
    ):
        stmt = select(CandidatoModel)
        if escolaridade:
            stmt = stmt.where(CandidatoModel.escolaridade == escolaridade.value)
        if situacao:
            stmt = stmt.where(CandidatoModel.situacao == situacao.value)
        if area_interesse:
            stmt = stmt.where(CandidatoModel.areas_interesse.contains([area_interesse]))
        if ativos:
            stmt = stmt.where(CandidatoModel.status == StatusCandidato.ATIVO.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_numero_processo(self, ano: int) -> str:
        stmt = (
            select(func.count())
            .select_from(CandidatoModel)
            .where(CandidatoModel.numero_processo.like(f"CAND/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"CAND/{ano}/{count + 1:04d}"

    @staticmethod
    def _to_domain(model: CandidatoModel) -> Candidato:
        return Candidato(
            id=model.id,
            numero_processo=model.numero_processo,
            citizen_id=model.citizen_id,
            data_registro=model.data_registro or date.today(),
            escolaridade=Escolaridade(model.escolaridade),
            situacao=SituacaoProfissional(model.situacao),
            areas_interesse=model.areas_interesse or [],
            experiencias=model.experiencias,
            habilidades=model.habilidades,
            status=StatusCandidato(model.status),
            observacoes=model.observacoes,
        )
