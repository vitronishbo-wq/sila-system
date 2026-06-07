from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.pescas.domain.enums import StatusLicenca


@dataclass
class LicencaPesca:
    id: UUID
    numero_licenca: str
    embarcacao_id: UUID
    titular_id: UUID
    data_emissao: date
    data_validade: date
    status: StatusLicenca
    modalidade_autorizada: str
    zona_pesca_id: UUID
    observacoes: str | None = None

    @classmethod
    def emitir(
        cls,
        *,
        numero_licenca: str,
        embarcacao_id: UUID,
        titular_id: UUID,
        data_emissao: date,
        data_validade: date,
        modalidade_autorizada: str,
        zona_pesca_id: UUID,
    ) -> LicencaPesca:
        return cls(
            id=uuid4(),
            numero_licenca=numero_licenca,
            embarcacao_id=embarcacao_id,
            titular_id=titular_id,
            data_emissao=data_emissao,
            data_validade=data_validade,
            status=StatusLicenca.DEFERIDA,
            modalidade_autorizada=modalidade_autorizada,
            zona_pesca_id=zona_pesca_id,
        )

    def suspender(self) -> None:
        self.status = StatusLicenca.SUSPENSA

    def cancelar(self) -> None:
        self.status = StatusLicenca.CANCELADA
