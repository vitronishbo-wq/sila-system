from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento


@dataclass
class IdosoVulneravel:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    citizen_id_idoso: UUID
    idade: int
    dependencia: bool
    precisa_cuidados: bool
    data_registro: datetime
    status: StatusAcompanhamento

    @classmethod
    def registrar(
        cls,
        *,
        codigo: str,
        beneficiario_id: UUID,
        citizen_id_idoso: UUID,
        idade: int,
        dependencia: bool,
        precisa_cuidados: bool,
    ) -> IdosoVulneravel:
        return cls(
            id=uuid4(),
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            citizen_id_idoso=citizen_id_idoso,
            idade=idade,
            dependencia=dependencia,
            precisa_cuidados=precisa_cuidados,
            data_registro=datetime.utcnow(),
            status=StatusAcompanhamento.ATIVO,
        )

    def encerrar_acompanhamento(self) -> None:
        self.status = StatusAcompanhamento.ENCERRADO
