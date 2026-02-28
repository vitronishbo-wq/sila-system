from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import EscolaRepositoryPort, MatriculaRepositoryPort
from app.modules.educacao.domain.models import Matricula, StatusMatricula
from app.modules.educacao.exceptions import (
    CitizenNotFoundError,
    EscolaNotFoundError,
    InvalidMatriculaStateError,
    MatriculaAlreadyExistsError,
)


class MatriculaService:
    """Service de matricula escolar integrando nucleo de identidade e tracking."""

    def __init__(
        self,
        matricula_repo: MatriculaRepositoryPort,
        escola_repo: EscolaRepositoryPort,
        citizen_repo: CitizenRepositoryPort,
        request_service: ServiceRequestLifecycleBridge,
    ):
        self.matricula_repo = matricula_repo
        self.escola_repo = escola_repo
        self.citizen_repo = citizen_repo
        self.request_service = request_service

    async def criar_matricula(
        self,
        *,
        citizen_id: UUID,
        escola_id: UUID,
        turma_id: UUID,
        ano_letivo_id: UUID,
        observacoes: Optional[str] = None,
    ) -> Matricula:
        citizen = await self.citizen_repo.get_by_id(citizen_id)
        if not citizen:
            raise CitizenNotFoundError(f"Cidadao {citizen_id} nao encontrado")

        escola = await self.escola_repo.get_by_id(escola_id)
        if not escola:
            raise EscolaNotFoundError(f"Escola {escola_id} nao encontrada")

        exists = await self.matricula_repo.exists_active_for_citizen(citizen_id, ano_letivo_id)
        if exists:
            raise MatriculaAlreadyExistsError(
                "Cidadao ja possui matricula ativa/pendente no ano letivo informado"
            )

        ano_atual = date.today().year
        numero_processo = await self.matricula_repo.next_numero_processo(ano_atual, escola_id)
        matricula = Matricula(
            id=uuid4(),
            numero_processo=numero_processo,
            citizen_id=citizen_id,
            escola_id=escola_id,
            turma_id=turma_id,
            ano_letivo_id=ano_letivo_id,
            data_matricula=date.today(),
            status=StatusMatricula.PENDENTE,
            observacoes=observacoes,
        )
        saved = await self.matricula_repo.save(matricula)
        await self.request_service.create_education_request(
            entity_id=saved.id,
            citizen_id=citizen_id,
            numero_processo=numero_processo,
            escola_nome=escola.nome,
            ano_letivo=str(ano_letivo_id),
        )
        return saved

    async def ativar_matricula(self, matricula_id: UUID) -> Matricula:
        matricula = await self.matricula_repo.get_by_id(matricula_id)
        if not matricula:
            raise InvalidMatriculaStateError("Matricula nao encontrada")

        try:
            matricula.ativar()
        except ValueError as exc:
            raise InvalidMatriculaStateError(str(exc)) from exc

        updated = await self.matricula_repo.save(matricula)
        await self.request_service.mark_education_request_completed(
            entity_id=matricula_id,
            actor_id=updated.citizen_id,
            metadata={"ativacao_data": date.today().isoformat()},
        )
        return updated

    async def listar_por_cidadao(
        self, citizen_id: UUID, ano_letivo_id: Optional[UUID] = None
    ) -> list[Matricula]:
        return await self.matricula_repo.get_by_citizen(citizen_id, ano_letivo_id)

