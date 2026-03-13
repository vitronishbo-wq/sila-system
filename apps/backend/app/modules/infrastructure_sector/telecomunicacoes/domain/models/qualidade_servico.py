from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusQualidadeServico, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.sla import SLA

@dataclass
class QualidadeServico:
    id: UUID
    codigo_medicao: str
    operadora_id: UUID
    servico: TipoServico
    data_medicao: date
    disponibilidade_percentual: float
    latencia_ms: float
    jitter_ms: float
    perda_pacotes_percentual: float
    velocidade_download_mbps: float
    velocidade_upload_mbps: float
    status: StatusQualidadeServico
    assinante_id: UUID | None = None
    sla_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_medicao: str, operadora_id: UUID, servico: TipoServico, data_medicao: date, disponibilidade_percentual: float, latencia_ms: float, jitter_ms: float, perda_pacotes_percentual: float, velocidade_download_mbps: float, velocidade_upload_mbps: float, assinante_id: UUID | None=None, sla_id: UUID | None=None, observacoes: str | None=None) -> 'QualidadeServico':
        if not 0 <= disponibilidade_percentual <= 100:
            raise ValueError('Disponibilidade deve estar entre 0 e 100')
        if latencia_ms < 0:
            raise ValueError('Latencia nao pode ser negativa')
        if jitter_ms < 0:
            raise ValueError('Jitter nao pode ser negativo')
        if not 0 <= perda_pacotes_percentual <= 100:
            raise ValueError('Perda de pacotes deve estar entre 0 e 100')
        if velocidade_download_mbps < 0 or velocidade_upload_mbps < 0:
            raise ValueError('Velocidades nao podem ser negativas')
        return cls(id=uuid4(), codigo_medicao=codigo_medicao.strip(), operadora_id=operadora_id, servico=servico, data_medicao=data_medicao, disponibilidade_percentual=disponibilidade_percentual, latencia_ms=latencia_ms, jitter_ms=jitter_ms, perda_pacotes_percentual=perda_pacotes_percentual, velocidade_download_mbps=velocidade_download_mbps, velocidade_upload_mbps=velocidade_upload_mbps, status=StatusQualidadeServico.ALERTA, assinante_id=assinante_id, sla_id=sla_id, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def avaliar_conformidade(self, sla: SLA | None=None) -> None:
        if sla is None:
            if self.disponibilidade_percentual >= 99.0 and self.latencia_ms <= 60:
                self.status = StatusQualidadeServico.CONFORME
            elif self.disponibilidade_percentual >= 95.0 and self.latencia_ms <= 120:
                self.status = StatusQualidadeServico.ALERTA
            else:
                self.status = StatusQualidadeServico.CRITICO
        else:
            conforme = self.disponibilidade_percentual >= sla.disponibilidade_min_percentual and self.latencia_ms <= sla.latencia_max_ms and (self.jitter_ms <= sla.jitter_max_ms) and (self.perda_pacotes_percentual <= sla.perda_pacotes_max_percentual) and (self.velocidade_download_mbps >= sla.velocidade_download_min_mbps) and (self.velocidade_upload_mbps >= sla.velocidade_upload_min_mbps)
            self.status = StatusQualidadeServico.CONFORME if conforme else StatusQualidadeServico.CRITICO
        self.ativo = self.status != StatusQualidadeServico.CRITICO

    def atualizar_status(self, status: StatusQualidadeServico) -> None:
        self.status = status
        self.ativo = status != StatusQualidadeServico.CRITICO