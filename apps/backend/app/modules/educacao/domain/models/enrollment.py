from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime

from apps.backend.app.modules.educacao.domain.enums import CanonicalStatus

@dataclass
class Enrollment:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    student_id: uuid.UUID
    institution_id: uuid.UUID
    academic_year: str
    grade: str | None = None
    status: CanonicalStatus = CanonicalStatus.PENDENTE
    started_at: date | None = None
    ended_at: date | None = None
    transfer_origin_id: uuid.UUID | None = None
    transfer_destination_id: uuid.UUID | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def activate(self):
        if self.status != CanonicalStatus.PENDENTE:
            raise ValueError("Só é possível ativar uma matrícula pendente.")
        self.status = CanonicalStatus.ATIVO
        self.started_at = date.today()

    def complete(self):
        if self.status != CanonicalStatus.ATIVO:
            raise ValueError("Só é possível completar uma matrícula ativa.")
        self.status = CanonicalStatus.CONCLUIDO
        self.ended_at = date.today()

    def transfer(self, new_enrollment_id: uuid.UUID):
        if self.status != CanonicalStatus.ATIVO:
            raise ValueError("Só é possível transferir uma matrícula ativa.")
        self.status = CanonicalStatus.TRANSFERIDO
        self.transfer_destination_id = new_enrollment_id
        self.ended_at = date.today()

    def cancel(self):
        if self.status in [CanonicalStatus.CONCLUIDO, CanonicalStatus.TRANSFERIDO]:
            raise ValueError("Não é possível cancelar uma matrícula finalizada ou transferida.")
        self.status = CanonicalStatus.CANCELADO
        self.ended_at = date.today()

    def suspend(self):
        if self.status != CanonicalStatus.ATIVO:
            raise ValueError("Só é possível suspender uma matrícula ativa.")
        self.status = CanonicalStatus.SUSPENSO
