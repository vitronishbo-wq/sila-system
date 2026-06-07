from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from uuid import UUID, uuid4


class WizardStatus(StrEnum):
    EM_CURSO = "em_curso"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    EXPIRADO = "expirado"


class PassoStatus(StrEnum):
    RASCUNHO = "rascunho"
    PREENCHIDO = "preenchido"
    VALIDADO = "validado"
    CONFIRMADO = "confirmado"


@dataclass
class WizardSession:
    id: UUID
    citizen_id: UUID
    status: WizardStatus
    passo_atual: int
    dados_estudante: dict | None = None
    dados_encarregado: dict | None = None
    selecao_escola: dict | None = None
    documentos: list[dict] | None = None
    resultado_elegibilidade: dict | None = None
    pagamento: dict | None = None
    matricula_id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    expires_at: datetime | None = None

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = datetime.utcnow() + timedelta(hours=24)

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def avancar_passo(self) -> None:
        if self.passo_atual < 7:
            self.passo_atual += 1

    def confirmar(self, matricula_id: UUID) -> None:
        self.status = WizardStatus.CONFIRMADO
        self.matricula_id = matricula_id

    def cancelar(self) -> None:
        self.status = WizardStatus.CANCELADO
