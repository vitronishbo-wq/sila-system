from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusOutorga,
    TipoOutorga,
)


@dataclass
class OutorgaEspectro:
    id: UUID
    numero_outorga: str
    operadora_id: UUID
    tipo_outorga: TipoOutorga
    faixa_inicio_mhz: float
    faixa_fim_mhz: float
    data_outorga: date
    status: StatusOutorga = StatusOutorga.EM_ANALISE
    data_validade: date | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def emitir(
        cls,
        *,
        numero_outorga: str,
        operadora_id: UUID,
        tipo_outorga: TipoOutorga,
        faixa_inicio_mhz: float,
        faixa_fim_mhz: float,
        data_outorga: date,
        data_validade: date | None = None,
        observacoes: str | None = None,
    ) -> OutorgaEspectro:
        if faixa_inicio_mhz < 0:
            raise ValueError("Faixa inicial nao pode ser negativa")
        if faixa_fim_mhz <= faixa_inicio_mhz:
            raise ValueError("Faixa final deve ser maior que a faixa inicial")
        if data_validade is not None and data_validade < data_outorga:
            raise ValueError("Data de validade deve ser posterior a data da outorga")
        return cls(
            id=uuid4(),
            numero_outorga=numero_outorga.strip(),
            operadora_id=operadora_id,
            tipo_outorga=tipo_outorga,
            faixa_inicio_mhz=faixa_inicio_mhz,
            faixa_fim_mhz=faixa_fim_mhz,
            data_outorga=data_outorga,
            data_validade=data_validade,
            status=StatusOutorga.EM_ANALISE,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusOutorga) -> None:
        self.status = status
        self.ativo = status not in {
            StatusOutorga.CANCELADA,
            StatusOutorga.INDEFERIDA,
            StatusOutorga.VENCIDA,
        }
