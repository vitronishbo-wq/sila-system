from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusIndicadorQualidade

@dataclass
class IndicadorQualidade:
    id: UUID
    codigo_indicador: str
    operadora_id: UUID
    referencia_ano: int
    referencia_mes: int
    total_medicoes: int
    disponibilidade_media_percentual: float
    latencia_media_ms: float
    jitter_medio_ms: float
    perda_pacotes_media_percentual: float
    conformidade_percentual: float
    data_calculo: date
    status: StatusIndicadorQualidade
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_indicador: str, operadora_id: UUID, referencia_ano: int, referencia_mes: int, total_medicoes: int, disponibilidade_media_percentual: float, latencia_media_ms: float, jitter_medio_ms: float, perda_pacotes_media_percentual: float, conformidade_percentual: float, observacoes: str | None=None) -> 'IndicadorQualidade':
        if referencia_ano < 2000:
            raise ValueError('Ano de referencia invalido')
        if not 1 <= referencia_mes <= 12:
            raise ValueError('Mes de referencia invalido')
        if total_medicoes <= 0:
            raise ValueError('Total de medicoes deve ser maior que zero')
        if not 0 <= conformidade_percentual <= 100:
            raise ValueError('Conformidade deve estar entre 0 e 100')
        status = cls.classificar_status(conformidade_percentual)
        return cls(id=uuid4(), codigo_indicador=codigo_indicador.strip(), operadora_id=operadora_id, referencia_ano=referencia_ano, referencia_mes=referencia_mes, total_medicoes=total_medicoes, disponibilidade_media_percentual=disponibilidade_media_percentual, latencia_media_ms=latencia_media_ms, jitter_medio_ms=jitter_medio_ms, perda_pacotes_media_percentual=perda_pacotes_media_percentual, conformidade_percentual=conformidade_percentual, data_calculo=date.today(), status=status, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    @staticmethod
    def classificar_status(conformidade_percentual: float) -> StatusIndicadorQualidade:
        if conformidade_percentual >= 95:
            return StatusIndicadorQualidade.BOM
        if conformidade_percentual >= 80:
            return StatusIndicadorQualidade.REGULAR
        return StatusIndicadorQualidade.CRITICO

    def atualizar_status(self, status: StatusIndicadorQualidade) -> None:
        self.status = status
        self.ativo = status != StatusIndicadorQualidade.CRITICO