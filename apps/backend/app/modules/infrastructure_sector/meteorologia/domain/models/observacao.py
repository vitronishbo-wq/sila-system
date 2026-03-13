from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.enums import AlertSeverity, AlertType, ObservationType

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class ObservacaoMeteorologica:
    """Entidade de dominio para observacao meteorologica."""
    TEMP_EXTREME_HIGH = 40.0
    TEMP_EXTREME_LOW = 0.0
    HUMIDITY_CRITICAL_LOW = 20.0
    HUMIDITY_CRITICAL_HIGH = 95.0
    PRESSURE_CRITICAL_LOW = 980.0
    WIND_DANGEROUS_HIGH = 80.0
    RAINFALL_HEAVY = 50.0

    def __init__(self, *, observacao_id: UUID | None=None, estacao_id: UUID | None=None, data_observacao: datetime | None=None, temperatura: float | None=None, humidade: float | None=None, pressao: float | None=None, velocidade_vento: float | None=None, direcao_vento: float | None=None, precipitacao: float | None=None, radiacao_solar: float | None=None, tipo: ObservationType=ObservationType.SURFACE, qualidade_dados: str | None=None, metadata: dict[str, Any] | None=None, created_at: datetime | None=None) -> None:
        self.id = observacao_id or uuid4()
        self.estacao_id = estacao_id
        self.data_observacao = data_observacao or _utcnow()
        self.temperatura = temperatura
        self.humidade = humidade
        self.pressao = pressao
        self.velocidade_vento = velocidade_vento
        self.direcao_vento = direcao_vento
        self.precipitacao = precipitacao
        self.radiacao_solar = radiacao_solar
        self.tipo = tipo
        self.qualidade_dados = qualidade_dados or 'VALIDADO'
        self.metadata = metadata or {}
        self.created_at = created_at or _utcnow()
        self._alertas: list[dict[str, Any]] = []

    @property
    def has_alerts(self) -> bool:
        return bool(self._alertas)

    @property
    def alerts(self) -> list[dict[str, Any]]:
        return list(self._alertas)

    def validar_dados(self) -> list[str]:
        warnings: list[str] = []
        if self.temperatura is not None and (self.temperatura < -50 or self.temperatura > 60):
            warnings.append(f'Temperatura fora de faixa razoavel: {self.temperatura}C')
        if self.humidade is not None and (not 0 <= self.humidade <= 100):
            warnings.append(f'Humidade invalida: {self.humidade}%')
        if self.pressao is not None and (not 870 <= self.pressao <= 1084):
            warnings.append(f'Pressao fora de faixa razoavel: {self.pressao} hPa')
        if self.velocidade_vento is not None:
            if self.velocidade_vento < 0:
                warnings.append(f'Velocidade do vento negativa: {self.velocidade_vento} km/h')
            if self.velocidade_vento > 300:
                warnings.append(f'Velocidade do vento extrema: {self.velocidade_vento} km/h')
        if self.direcao_vento is not None and (not 0 <= self.direcao_vento <= 360):
            warnings.append(f'Direcao do vento invalida: {self.direcao_vento}')
        if self.precipitacao is not None and self.precipitacao < 0:
            warnings.append(f'Precipitacao negativa: {self.precipitacao} mm')
        return warnings

    def analisar_severidade(self) -> list[dict[str, Any]]:
        self._alertas = []
        if self.temperatura is not None and self.temperatura >= self.TEMP_EXTREME_HIGH:
            severity = AlertSeverity.EXTREME if self.temperatura >= 45 else AlertSeverity.HIGH
            self._alertas.append({'tipo': AlertType.HEAT_WAVE.value, 'severidade': severity.value, 'mensagem': f'Temperatura critica: {self.temperatura}C', 'valor': self.temperatura, 'limite': self.TEMP_EXTREME_HIGH})
        if self.temperatura is not None and self.temperatura <= self.TEMP_EXTREME_LOW:
            severity = AlertSeverity.HIGH if self.temperatura <= -5 else AlertSeverity.MODERATE
            self._alertas.append({'tipo': AlertType.FROST.value, 'severidade': severity.value, 'mensagem': f'Temperatura muito baixa: {self.temperatura}C', 'valor': self.temperatura, 'limite': self.TEMP_EXTREME_LOW})
        if self.humidade is not None and self.humidade <= self.HUMIDITY_CRITICAL_LOW:
            severity = AlertSeverity.EXTREME if self.humidade <= 10 else AlertSeverity.HIGH
            self._alertas.append({'tipo': AlertType.DROUGHT.value, 'severidade': severity.value, 'mensagem': f'Humidade critica: {self.humidade}%', 'valor': self.humidade, 'limite': self.HUMIDITY_CRITICAL_LOW})
        if self.velocidade_vento is not None and self.velocidade_vento >= self.WIND_DANGEROUS_HIGH:
            severity = AlertSeverity.EXTREME if self.velocidade_vento >= 120 else AlertSeverity.HIGH
            self._alertas.append({'tipo': AlertType.STRONG_WIND.value, 'severidade': severity.value, 'mensagem': f'Vento perigoso: {self.velocidade_vento} km/h', 'valor': self.velocidade_vento, 'limite': self.WIND_DANGEROUS_HIGH})
        if self.pressao is not None and self.pressao <= self.PRESSURE_CRITICAL_LOW:
            self._alertas.append({'tipo': AlertType.STORM.value, 'severidade': AlertSeverity.MODERATE.value, 'mensagem': f'Pressao muito baixa: {self.pressao} hPa', 'valor': self.pressao, 'limite': self.PRESSURE_CRITICAL_LOW})
        if self.precipitacao is not None and self.precipitacao >= self.RAINFALL_HEAVY:
            severity = AlertSeverity.HIGH if self.precipitacao >= 100 else AlertSeverity.MODERATE
            self._alertas.append({'tipo': AlertType.HEAVY_RAIN.value, 'severidade': severity.value, 'mensagem': f'Precipitacao intensa: {self.precipitacao} mm', 'valor': self.precipitacao, 'limite': self.RAINFALL_HEAVY})
        return list(self._alertas)

    def to_dict(self) -> dict[str, Any]:
        return {'id': str(self.id), 'estacao_id': str(self.estacao_id) if self.estacao_id else None, 'data_observacao': self.data_observacao.isoformat() if self.data_observacao else None, 'leituras': {'temperatura': self.temperatura, 'humidade': self.humidade, 'pressao': self.pressao, 'velocidade_vento': self.velocidade_vento, 'direcao_vento': self.direcao_vento, 'precipitacao': self.precipitacao, 'radiacao_solar': self.radiacao_solar}, 'tipo': self.tipo.value, 'qualidade_dados': self.qualidade_dados, 'alertas': list(self._alertas), 'has_alerts': self.has_alerts, 'created_at': self.created_at.isoformat() if self.created_at else None}