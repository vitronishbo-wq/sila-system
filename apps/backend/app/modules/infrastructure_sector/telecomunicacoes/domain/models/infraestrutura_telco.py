from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusInfraestrutura,
    TipoInfraestrutura,
)


@dataclass
class InfraestruturaTelco:
    id: UUID
    codigo_infra: str
    operadora_id: UUID
    tipo: TipoInfraestrutura
    identificador: str
    municipio: str
    provincia: str
    data_implantacao: date
    status: StatusInfraestrutura = StatusInfraestrutura.PLANEADA
    latitude: float | None = None
    longitude: float | None = None
    capacidade: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(
        cls,
        *,
        codigo_infra: str,
        operadora_id: UUID,
        tipo: TipoInfraestrutura,
        identificador: str,
        municipio: str,
        provincia: str,
        data_implantacao: date,
        latitude: float | None = None,
        longitude: float | None = None,
        capacidade: str | None = None,
        observacoes: str | None = None,
    ) -> InfraestruturaTelco:
        if len(identificador.strip()) < 3:
            raise ValueError("Identificador da infraestrutura deve ter pelo menos 3 caracteres")
        if latitude is not None and (not -90 <= latitude <= 90):
            raise ValueError("Latitude invalida")
        if longitude is not None and (not -180 <= longitude <= 180):
            raise ValueError("Longitude invalida")
        if data_implantacao > date.today():
            raise ValueError("Data de implantacao nao pode ser futura")
        return cls(
            id=uuid4(),
            codigo_infra=codigo_infra.strip(),
            operadora_id=operadora_id,
            tipo=tipo,
            identificador=identificador.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            data_implantacao=data_implantacao,
            status=StatusInfraestrutura.PLANEADA,
            latitude=latitude,
            longitude=longitude,
            capacidade=capacidade.strip() if capacidade else None,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusInfraestrutura) -> None:
        self.status = status
        self.ativo = status != StatusInfraestrutura.DESATIVADA
