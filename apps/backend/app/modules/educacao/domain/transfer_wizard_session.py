from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional


class TransferWizardStatus(str, Enum):
    EM_CURSO = "em_curso"
    ELEGIVEL = "elegivel"
    RESERVADO = "reservado"
    CONCLUIDO = "concluido"
    EXPIRADO = "expirado"
    CANCELADO = "cancelado"


class PassoStatus(str, Enum):
    RASCUNHO = "rascunho"
    PREENCHIDO = "preenchido"
    CONFIRMADO = "confirmado"


class TransferWizardSession:
    def __init__(
        self,
        *,
        id: uuid.UUID,
        citizen_id: uuid.UUID,
        status: TransferWizardStatus = TransferWizardStatus.EM_CURSO,
        passo_atual: int = 1,
        origem_escola_id: uuid.UUID | None = None,
        origem_turma_id: uuid.UUID | None = None,
        origem_classe: str | None = None,
        destino_escola_id: uuid.UUID | None = None,
        destino_turma_id: uuid.UUID | None = None,
        destino_classe: str | None = None,
        destino_turno: str | None = None,
        motivo: str | None = None,
        elegibilidade: dict[str, Any] | None = None,
        reserva_id: uuid.UUID | None = None,
        transferencia_id: uuid.UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        expires_at: datetime | None = None,
    ):
        self.id = id
        self.citizen_id = citizen_id
        self.status = status
        self.passo_atual = passo_atual
        self.origem_escola_id = origem_escola_id
        self.origem_turma_id = origem_turma_id
        self.origem_classe = origem_classe
        self.destino_escola_id = destino_escola_id
        self.destino_turma_id = destino_turma_id
        self.destino_classe = destino_classe
        self.destino_turno = destino_turno
        self.motivo = motivo
        self.elegibilidade = elegibilidade
        self.reserva_id = reserva_id
        self.transferencia_id = transferencia_id
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at
        self.expires_at = expires_at or (datetime.now(timezone.utc) + timedelta(hours=48))

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def confirmar(self, transferencia_id: uuid.UUID) -> None:
        self.transferencia_id = transferencia_id
        self.status = TransferWizardStatus.CONCLUIDO
        self.passo_atual = 5
        self.updated_at = datetime.now(timezone.utc)
