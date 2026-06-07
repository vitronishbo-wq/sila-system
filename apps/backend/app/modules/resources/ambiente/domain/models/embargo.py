from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.ambiente.domain.enums import StatusEmbargo


@dataclass
class Embargo:
    id: UUID
    numero_embargo: str
    numero_auto_infracao: str
    motivo: str
    status: StatusEmbargo
    data_aplicacao: date
    data_levantamento: date | None = None
    observacoes: str | None = None

    @classmethod
    def aplicar(cls, *, numero_auto_infracao: str, motivo: str) -> Embargo:
        if not motivo.strip():
            raise ValueError("Motivo do embargo e obrigatorio")
        return cls(
            id=uuid4(),
            numero_embargo="",
            numero_auto_infracao=numero_auto_infracao,
            motivo=motivo.strip(),
            status=StatusEmbargo.ATIVO,
            data_aplicacao=date.today(),
        )

    def suspender(self, motivo: str) -> None:
        if self.status != StatusEmbargo.ATIVO:
            raise ValueError("Apenas embargo ativo pode ser suspenso")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao do embargo e obrigatorio")
        self.status = StatusEmbargo.SUSPENSO
        self.observacoes = motivo.strip()

    def levantar(self, observacoes: str | None = None) -> None:
        if self.status == StatusEmbargo.LEVANTADO:
            raise ValueError("Embargo ja levantado")
        self.status = StatusEmbargo.LEVANTADO
        self.data_levantamento = date.today()
        self.observacoes = observacoes.strip() if observacoes else None
