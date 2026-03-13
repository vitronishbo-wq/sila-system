from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusSLA, TipoServico

@dataclass
class SLA:
    id: UUID
    codigo_sla: str
    operadora_id: UUID
    nome: str
    servico: TipoServico
    disponibilidade_min_percentual: float
    latencia_max_ms: float
    jitter_max_ms: float
    perda_pacotes_max_percentual: float
    velocidade_download_min_mbps: float
    velocidade_upload_min_mbps: float
    data_inicio: date
    status: StatusSLA = StatusSLA.ATIVO
    data_fim: date | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def criar(cls, *, codigo_sla: str, operadora_id: UUID, nome: str, servico: TipoServico, disponibilidade_min_percentual: float, latencia_max_ms: float, jitter_max_ms: float, perda_pacotes_max_percentual: float, velocidade_download_min_mbps: float, velocidade_upload_min_mbps: float, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> 'SLA':
        if len(nome.strip()) < 3:
            raise ValueError('Nome do SLA deve ter pelo menos 3 caracteres')
        if not 0 <= disponibilidade_min_percentual <= 100:
            raise ValueError('Disponibilidade minima deve estar entre 0 e 100')
        if latencia_max_ms <= 0:
            raise ValueError('Latencia maxima deve ser maior que zero')
        if jitter_max_ms < 0:
            raise ValueError('Jitter maximo nao pode ser negativo')
        if not 0 <= perda_pacotes_max_percentual <= 100:
            raise ValueError('Perda de pacotes maxima deve estar entre 0 e 100')
        if velocidade_download_min_mbps < 0 or velocidade_upload_min_mbps < 0:
            raise ValueError('Velocidades minimas nao podem ser negativas')
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError('Data fim do SLA deve ser posterior a data inicio')
        return cls(id=uuid4(), codigo_sla=codigo_sla.strip(), operadora_id=operadora_id, nome=nome.strip(), servico=servico, disponibilidade_min_percentual=disponibilidade_min_percentual, latencia_max_ms=latencia_max_ms, jitter_max_ms=jitter_max_ms, perda_pacotes_max_percentual=perda_pacotes_max_percentual, velocidade_download_min_mbps=velocidade_download_min_mbps, velocidade_upload_min_mbps=velocidade_upload_min_mbps, data_inicio=data_inicio, data_fim=data_fim, status=StatusSLA.ATIVO, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusSLA) -> None:
        self.status = status
        self.ativo = status == StatusSLA.ATIVO