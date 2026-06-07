from __future__ import annotations

import uuid
from datetime import timezone
from datetime import datetime
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.marketplace.marketplace_service import (
    MatchingService,
    SeatReservationService,
    StudentProfile,
)
from apps.backend.app.modules.educacao.domain.transfer_wizard_session import (
    TransferWizardSession,
    TransferWizardStatus,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_institution_repository import (
    MarketplaceInstitutionRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_vacancy_repository import (
    MarketplaceVacancyRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.seat_reservation_repository import (
    SeatReservationRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.transfer_wizard_repository import (
    TransferWizardRepository,
)


class TransferWizardService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo = TransferWizardRepository(session)
        self._institution_repo = MarketplaceInstitutionRepository(session)
        self._vacancy_repo = MarketplaceVacancyRepository(session)
        self._reservation_repo = SeatReservationRepository(session)
        self._reservation_service = SeatReservationService(self._reservation_repo, self._vacancy_repo)
        self._matching_service = MatchingService(self._institution_repo, self._vacancy_repo)

    async def iniciar(self, citizen_id: uuid.UUID) -> TransferWizardSession:
        session = TransferWizardSession(
            id=uuid.uuid4(),
            citizen_id=citizen_id,
        )
        return await self._repo.create(session)

    async def obter(self, wizard_id: uuid.UUID) -> Optional[TransferWizardSession]:
        return await self._repo.get_by_id(wizard_id)

    async def listar(self, citizen_id: uuid.UUID) -> list[TransferWizardSession]:
        return await self._repo.list_by_citizen(citizen_id)

    async def passo1_origem(
        self,
        wizard_id: uuid.UUID,
        origem_escola_id: uuid.UUID,
        origem_classe: str,
    ) -> TransferWizardSession:
        session = await self._repo.get_by_id(wizard_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        session.origem_escola_id = origem_escola_id
        session.origem_classe = origem_classe
        session.passo_atual = 2
        session.updated_at = datetime.now(timezone.utc)
        await self._repo.save(session)
        return session

    async def passo2_destino(
        self,
        wizard_id: uuid.UUID,
        destino_escola_id: uuid.UUID,
        destino_classe: str,
        destino_turno: str,
        motivo: str,
    ) -> TransferWizardSession:
        session = await self._repo.get_by_id(wizard_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        session.destino_escola_id = destino_escola_id
        session.destino_classe = destino_classe
        session.destino_turno = destino_turno
        session.motivo = motivo
        session.passo_atual = 3
        session.updated_at = datetime.now(timezone.utc)
        await self._repo.save(session)
        return session

    async def passo3_elegibilidade(
        self, wizard_id: uuid.UUID, ano_letivo: str = "2026"
    ) -> tuple[TransferWizardSession, dict[str, Any]]:
        session = await self._repo.get_by_id(wizard_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        if not session.destino_escola_id:
            raise ValueError("Passo 2 (destino) deve ser concluído primeiro")

        origem_inst = await self._institution_repo.get_by_institution_id(session.origem_escola_id)
        destino_inst = await self._institution_repo.get_by_institution_id(session.destino_escola_id)

        student = StudentProfile(
            student_id=session.citizen_id,
            provincia=destino_inst.provincia if destino_inst else "",
            municipio=destino_inst.municipio if destino_inst else "",
            bairro=destino_inst.bairro if destino_inst else "",
            classe=session.destino_classe,
            turno_preferido=session.destino_turno,
        )
        score_result = await self._matching_service.compute_score(
            student, session.destino_escola_id, ano_letivo
        )
        score = score_result["score"]
        motivos = score_result["motivos"]

        vacancys, _ = await self._vacancy_repo.search(
            instituicao_id=session.destino_escola_id,
            classe=session.destino_classe,
            turno=session.destino_turno,
        )
        tem_vaga = len(vacancys) > 0

        mesma_rede = bool(
            origem_inst and destino_inst and origem_inst.tipo == destino_inst.tipo
        ) if origem_inst and destino_inst else False
        classes_compativeis = session.origem_classe == session.destino_classe

        eligibility = {
            "elegivel": score >= 40 and tem_vaga,
            "score": max(0, min(100, score)),
            "motivos": motivos,
            "tem_vaga": tem_vaga,
            "mesma_rede": mesma_rede,
            "classes_compativeis": classes_compativeis,
            "ano_letivo": ano_letivo,
        }

        session.elegibilidade = eligibility
        session.passo_atual = 4
        session.status = TransferWizardStatus.ELEGIVEL
        session.updated_at = datetime.now(timezone.utc)
        await self._repo.save(session)
        return session, eligibility

    async def passo4_reservar(
        self,
        wizard_id: uuid.UUID,
        student_id: uuid.UUID,
        ano_letivo: str = "2026",
    ) -> tuple[TransferWizardSession, dict]:
        session = await self._repo.get_by_id(wizard_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        if not session.elegibilidade or not session.elegibilidade.get("elegivel"):
            raise ValueError("Candidatura não elegível")

        reserva = await self._reservation_service.create_reservation(
            student_id=student_id,
            institution_id=session.destino_escola_id,
            classe=session.destino_classe or "",
            turno=session.destino_turno or "",
            ano_letivo=ano_letivo,
        )
        if not reserva.get("criada"):
            raise ValueError(reserva.get("erro", "Falha ao criar reserva"))

        session.reserva_id = reserva["reservation_id"]
        session.passo_atual = 5
        session.status = TransferWizardStatus.RESERVADO
        session.updated_at = datetime.now(timezone.utc)
        await self._repo.save(session)
        return session, reserva

    async def passo5_confirmar(
        self,
        wizard_id: uuid.UUID,
        transferencia_id: uuid.UUID,
    ) -> TransferWizardSession:
        session = await self._repo.get_by_id(wizard_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        session.confirmar(transferencia_id)
        if session.reserva_id:
            await self._reservation_service.confirm_reservation(session.reserva_id)
        await self._repo.save(session)
        return session

    async def cancelar(self, wizard_id: uuid.UUID) -> TransferWizardSession:
        session = await self._repo.get_by_id(wizard_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        session.status = TransferWizardStatus.CANCELADO
        session.updated_at = datetime.now(timezone.utc)
        if session.reserva_id:
            await self._reservation_repo.cancel(session.reserva_id)
        await self._repo.save(session)
        return session
