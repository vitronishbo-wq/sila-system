from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusEspectro,
    TipoEspectro,
    TipoServico,
)


@dataclass
class Espectro:
    id: UUID
    codigo_espectro: str
    tipo: TipoEspectro
    frequencia_inicial_mhz: float
    frequencia_final_mhz: float
    largura_banda_mhz: float
    servico_principal: TipoServico
    municipio: str
    provincia: str
    status: StatusEspectro = StatusEspectro.DISPONIVEL
    outorga_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(
        cls,
        *,
        codigo_espectro: str,
        tipo: TipoEspectro,
        frequencia_inicial_mhz: float,
        frequencia_final_mhz: float,
        servico_principal: TipoServico,
        municipio: str,
        provincia: str,
        outorga_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Espectro:
        if frequencia_inicial_mhz < 0:
            raise ValueError("Frequencia inicial nao pode ser negativa")
        if frequencia_final_mhz <= frequencia_inicial_mhz:
            raise ValueError("Frequencia final deve ser maior que a inicial")
        largura_banda = frequencia_final_mhz - frequencia_inicial_mhz
        status = StatusEspectro.OUTORGADO if outorga_id else StatusEspectro.DISPONIVEL
        return cls(
            id=uuid4(),
            codigo_espectro=codigo_espectro.strip(),
            tipo=tipo,
            frequencia_inicial_mhz=frequencia_inicial_mhz,
            frequencia_final_mhz=frequencia_final_mhz,
            largura_banda_mhz=largura_banda,
            servico_principal=servico_principal,
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            status=status,
            outorga_id=outorga_id,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def vincular_outorga(self, outorga_id: UUID) -> None:
        self.outorga_id = outorga_id
        self.status = StatusEspectro.OUTORGADO
        self.ativo = True

    def atualizar_status(self, status: StatusEspectro) -> None:
        self.status = status
        self.ativo = status != StatusEspectro.RESERVA
