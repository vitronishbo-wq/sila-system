from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import NaturezaVoo, RegrasVoo, StatusVoo, TipoVoo

@dataclass
class Voo:
    numero_voo: str
    empresa_id: UUID
    aeronave_id: UUID
    aeroporto_origem_id: UUID
    aeroporto_destino_id: UUID
    data_hora_partida_programada: datetime
    data_hora_chegada_programada: datetime
    tipo: TipoVoo
    natureza: NaturezaVoo
    regras: RegrasVoo
    passageiros: int
    tripulantes: list[dict]
    id: UUID = field(default_factory=uuid4)
    status: StatusVoo = StatusVoo.PROGRAMADO
    data_hora_partida_real: datetime | None = None
    data_hora_chegada_real: datetime | None = None
    historico_status: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.numero_voo = self.numero_voo.strip().upper()
        if self.passageiros < 0:
            raise ValueError('Passageiros nao pode ser negativo')
        if self.data_hora_chegada_programada <= self.data_hora_partida_programada:
            raise ValueError('Chegada programada deve ser maior que partida programada')

    def atualizar_status(self, novo_status: StatusVoo, motivo: str | None=None) -> None:
        self.status = novo_status
        self.historico_status.append({'timestamp': datetime.utcnow().isoformat(), 'status': novo_status.value, 'motivo': motivo})

    def registrar_partida(self, data_hora: datetime) -> int:
        self.data_hora_partida_real = data_hora
        atraso = int((data_hora - self.data_hora_partida_programada).total_seconds() // 60)
        if atraso > 15:
            self.atualizar_status(StatusVoo.ATRASADO, f'Atraso de {atraso} minutos')
        self.atualizar_status(StatusVoo.DECOLADO)
        self.atualizar_status(StatusVoo.EM_VOO)
        return max(0, atraso)

    def registrar_chegada(self, data_hora: datetime) -> float:
        self.data_hora_chegada_real = data_hora
        self.atualizar_status(StatusVoo.POUSADO)
        return self.tempo_voo_horas() or 0.0

    def tempo_voo_horas(self) -> float | None:
        if not self.data_hora_partida_real or not self.data_hora_chegada_real:
            return None
        return (self.data_hora_chegada_real - self.data_hora_partida_real).total_seconds() / 3600