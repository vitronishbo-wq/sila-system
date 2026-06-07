from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import (
    CategoriaAeronave,
    StatusAeronavegabilidade,
    TipoAeronave,
)


@dataclass
class Aeronave:
    matricula: str
    tipo: TipoAeronave
    categoria: CategoriaAeronave
    fabricante: str
    modelo: str
    numero_serie: str
    ano_fabricacao: int
    proprietario_cpf_cnpj: str
    capacidade_passageiros: int = 0
    autonomia_km: float = 0.0
    peso_maximo_decolagem_kg: float = 0.0
    operador_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    data_registro: datetime = field(default_factory=datetime.utcnow)
    status_aeronavegabilidade: StatusAeronavegabilidade = StatusAeronavegabilidade.VALIDO
    horas_voadas_total: float = 0.0
    ciclos_total: int = 0
    ultima_inspecao: datetime | None = None
    proxima_inspecao: datetime | None = None

    def __post_init__(self) -> None:
        self.matricula = self.matricula.strip().upper()
        self.numero_serie = self.numero_serie.strip().upper()
        if self.ano_fabricacao < 1903:
            raise ValueError("Ano de fabricacao invalido")
        if not self.matricula:
            raise ValueError("Matricula obrigatoria")

    def registrar_voo(self, horas: float, ciclos: int = 1) -> None:
        if horas <= 0:
            raise ValueError("Horas de voo devem ser positivas")
        if ciclos <= 0:
            raise ValueError("Ciclos devem ser positivos")
        self.horas_voadas_total += horas
        self.ciclos_total += ciclos
        self._avaliar_aeronavegabilidade()

    def realizar_inspecao(self, quando: datetime) -> None:
        self.ultima_inspecao = quando
        self.proxima_inspecao = quando + timedelta(days=365)
        self.status_aeronavegabilidade = StatusAeronavegabilidade.VALIDO

    def _avaliar_aeronavegabilidade(self) -> None:
        if self.proxima_inspecao and datetime.utcnow() >= self.proxima_inspecao:
            self.status_aeronavegabilidade = StatusAeronavegabilidade.SUSPENSO

    def idade(self) -> int:
        return max(0, datetime.utcnow().year - self.ano_fabricacao)
