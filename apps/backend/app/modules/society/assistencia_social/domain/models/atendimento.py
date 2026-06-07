from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.society.assistencia_social.domain.enums import (
    StatusAcompanhamento,
    TipoAtendimento,
)


@dataclass
class Atendimento:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    tipo: TipoAtendimento
    descricao: str
    responsavel_id: UUID
    data_atendimento: datetime
    status: StatusAcompanhamento
    encaminhamentos: list[dict]

    @classmethod
    def registrar(
        cls,
        *,
        codigo: str,
        beneficiario_id: UUID,
        tipo: TipoAtendimento,
        descricao: str,
        responsavel_id: UUID,
        encaminhamentos: list[dict] | None = None,
    ) -> Atendimento:
        return cls(
            id=uuid4(),
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            tipo=tipo,
            descricao=descricao,
            responsavel_id=responsavel_id,
            data_atendimento=datetime.utcnow(),
            status=StatusAcompanhamento.ATIVO,
            encaminhamentos=encaminhamentos or [],
        )

    def encerrar(self) -> None:
        self.status = StatusAcompanhamento.ENCERRADO
