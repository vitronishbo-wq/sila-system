from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import TipoAeroporto


@dataclass
class Aeroporto:
    codigo_iata: str
    codigo_icao: str
    nome: str
    tipo: TipoAeroporto
    municipio_id: UUID
    coordenadas: dict[str, float]
    altitude_m: int
    fuso_horario: str
    administracao: str
    id: UUID = field(default_factory=uuid4)
    capacidade_anual: int = 0
    movimento_anual: int = 0

    def __post_init__(self) -> None:
        self.codigo_iata = self.codigo_iata.strip().upper()
        self.codigo_icao = self.codigo_icao.strip().upper()

    def registrar_movimento(self, passageiros: int) -> None:
        if passageiros < 0:
            raise ValueError("Passageiros nao pode ser negativo")
        self.movimento_anual += passageiros

    def ocupacao_percentual(self) -> float:
        if self.capacidade_anual <= 0:
            return 0.0
        return self.movimento_anual / self.capacidade_anual * 100
