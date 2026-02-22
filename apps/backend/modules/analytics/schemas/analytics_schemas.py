"""
Schemas Pydantic para o módulo de Analytics.

Define estruturas de dados para sistema de analytics, incluindo:
- Dashboards executivos e métricas estratégicas
- Relatórios personalizáveis e análises de dados
- Métricas em tempo real e indicadores de performance
- Configurações de alertas e thresholds
- Exportação de dados em múltiplos formatos
- Análise de tendências e forecasting
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class MetricType(str, Enum):
    """Tipos de métricas disponíveis."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class MetricCategory(str, Enum):
    """Categorias de métricas do sistema."""

    USER_ACTIVITY = "user_activity"
    SYSTEM_PERFORMANCE = "system_performance"
    BUSINESS_METRICS = "business_metrics"
    SECURITY_EVENTS = "security_events"
    FINANCIAL_INDICATORS = "financial_indicators"


class ReportType(str, Enum):
    """Tipos de relatórios disponíveis."""

    EXECUTIVE_DASHBOARD = "executive_dashboard"
    USER_ACTIVITY = "user_activity"
    SYSTEM_PERFORMANCE = "system_performance"
    MODULE_USAGE = "module_usage"
    SECURITY_AUDIT = "security_audit"
    FINANCIAL_SUMMARY = "financial_summary"


class ReportFormat(str, Enum):
    """Formatos de exportação de relatórios."""

    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    HTML = "html"


class DashboardType(str, Enum):
    """Tipos de dashboards disponíveis."""

    EXECUTIVE = "executive"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    SECURITY = "security"


class TimeRange(str, Enum):
    """Períodos de tempo para análises."""

    LAST_HOUR = "last_hour"
    LAST_24_HOURS = "last_24_hours"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"
    LAST_YEAR = "last_year"
    CUSTOM = "custom"


class MetricBase(BaseModel):
    """Schema base para métricas."""

    name: str = Field(..., min_length=1, max_length=255, description="Nome da métrica")
    description: str = Field(..., max_length=1000, description="Descrição detalhada")
    category: MetricCategory = Field(..., description="Categoria da métrica")
    metric_type: MetricType = Field(..., description="Tipo da métrica")
    unit: str = Field(..., description="Unidade de medida")
    is_active: bool = Field(True, description="Se a métrica está ativa")


class MetricCreate(MetricBase):
    """Schema para criação de métricas."""

    aggregation_function: str = Field(
        ..., description="Função de agregação (sum, avg, count, etc.)"
    )
    refresh_interval_seconds: int = Field(
        default=300, ge=30, description="Intervalo de atualização em segundos"
    )


class MetricRead(MetricBase):
    """Schema para leitura de métricas."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    last_calculated_at: Optional[datetime] = None
    current_value: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class MetricValueBase(BaseModel):
    """Schema base para valores de métricas."""

    metric_id: UUID = Field(..., description="ID da métrica")
    value: float = Field(..., description="Valor da métrica")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Momento da medição"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados adicionais"
    )


class MetricValueCreate(MetricValueBase):
    """Schema para criação de valores de métricas."""


class MetricValueRead(MetricValueBase):
    """Schema para leitura de valores de métricas."""

    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardBase(BaseModel):
    """Schema base para dashboards."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="Nome do dashboard"
    )
    description: str = Field(..., max_length=1000, description="Descrição do dashboard")
    dashboard_type: DashboardType = Field(..., description="Tipo do dashboard")
    is_public: bool = Field(False, description="Se o dashboard é público")
    refresh_interval_seconds: int = Field(
        default=300, ge=30, description="Intervalo de atualização"
    )


class DashboardCreate(DashboardBase):
    """Schema para criação de dashboards."""

    metric_ids: List[UUID] = Field(
        ..., min_length=1, description="IDs das métricas a incluir"
    )
    layout_config: Dict[str, Any] = Field(
        default_factory=dict, description="Configuração de layout"
    )


class DashboardRead(DashboardBase):
    """Schema para leitura de dashboards."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    metric_count: int = Field(0, description="Número de métricas")
    last_accessed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DashboardData(BaseModel):
    """Schema para dados de dashboard."""

    dashboard_id: UUID
    dashboard_name: str
    last_updated: datetime
    metrics: List[Dict[str, Any]]
    summary_stats: Dict[str, Any]


class ReportBase(BaseModel):
    """Schema base para relatórios."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="Nome do relatório"
    )
    description: str = Field(..., max_length=1000, description="Descrição do relatório")
    report_type: ReportType = Field(..., description="Tipo do relatório")
    is_scheduled: bool = Field(False, description="Se é relatório agendado")
    format: ReportFormat = Field(
        default=ReportFormat.PDF, description="Formato de exportação"
    )


class ReportCreate(ReportBase):
    """Schema para criação de relatórios."""

    metric_ids: List[UUID] = Field(..., min_length=1, description="Métricas a incluir")
    filters: Dict[str, Any] = Field(
        default_factory=dict, description="Filtros aplicados"
    )
    time_range: TimeRange = Field(
        default=TimeRange.LAST_30_DAYS, description="Período de análise"
    )
    schedule_config: Optional[Dict[str, Any]] = Field(
        None, description="Configuração de agendamento"
    )


class ReportRead(ReportBase):
    """Schema para leitura de relatórios."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    last_generated_at: Optional[datetime] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ReportGenerationRequest(BaseModel):
    """Schema para solicitação de geração de relatório."""

    report_id: UUID = Field(..., description="ID do relatório")
    time_range: TimeRange = Field(..., description="Período para análise")
    custom_start_date: Optional[datetime] = Field(
        None, description="Data inicial personalizada"
    )
    custom_end_date: Optional[datetime] = Field(
        None, description="Data final personalizada"
    )
    filters: Dict[str, Any] = Field(
        default_factory=dict, description="Filtros adicionais"
    )
    format: ReportFormat = Field(
        default=ReportFormat.PDF, description="Formato de saída"
    )
    include_charts: bool = Field(True, description="Incluir gráficos")
    include_raw_data: bool = Field(False, description="Incluir dados brutos")


class ReportData(BaseModel):
    """Schema para dados de relatório gerado."""

    report_id: UUID
    report_name: str
    generated_at: datetime
    time_range: Dict[str, Any]
    summary: Dict[str, Any]
    metrics: List[Dict[str, Any]]
    charts: List[Dict[str, Any]]
    raw_data: Optional[List[Dict[str, Any]]] = None
    file_url: Optional[str] = None


class AlertRuleBase(BaseModel):
    """Schema base para regras de alerta."""

    name: str = Field(..., min_length=1, max_length=255, description="Nome da regra")
    description: str = Field(..., max_length=1000, description="Descrição da regra")
    metric_id: UUID = Field(..., description="ID da métrica monitorada")
    condition: str = Field(
        ..., description="Condição (greater_than, less_than, equals)"
    )
    threshold_value: float = Field(..., description="Valor limite")
    severity: str = Field(
        ..., description="Severidade (info, warning, error, critical)"
    )


class AlertRuleCreate(AlertRuleBase):
    """Schema para criação de regras de alerta."""

    notification_channels: List[str] = Field(
        default_factory=list, description="Canais de notificação"
    )
    cooldown_minutes: int = Field(
        default=15, ge=1, description="Tempo de cooldown entre alertas"
    )
    is_active: bool = Field(True, description="Se a regra está ativa")


class AlertRuleRead(AlertRuleBase):
    """Schema para leitura de regras de alerta."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    last_triggered_at: Optional[datetime] = None
    trigger_count: int = Field(0, description="Número de vezes que disparou")

    model_config = ConfigDict(from_attributes=True)


class AlertBase(BaseModel):
    """Schema base para alertas ativos."""

    alert_rule_id: UUID = Field(..., description="ID da regra que disparou")
    metric_value: float = Field(..., description="Valor que causou o alerta")
    message: str = Field(..., max_length=1000, description="Mensagem do alerta")
    severity: str = Field(..., description="Severidade do alerta")


class AlertCreate(AlertBase):
    """Schema para criação de alertas."""

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados do alerta"
    )


class AlertRead(AlertBase):
    """Schema para leitura de alertas."""

    id: UUID
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AnalyticsFilters(BaseModel):
    """Schema para filtros de analytics."""

    metric_ids: Optional[List[UUID]] = Field(
        None, description="IDs das métricas específicas"
    )
    categories: Optional[List[MetricCategory]] = Field(
        None, description="Categorias de métricas"
    )
    time_range: TimeRange = Field(
        default=TimeRange.LAST_30_DAYS, description="Período de análise"
    )
    start_date: Optional[datetime] = Field(
        None, description="Data inicial personalizada"
    )
    end_date: Optional[datetime] = Field(None, description="Data final personalizada")
    group_by: Optional[str] = Field(
        None, description="Agrupamento (hour, day, week, month)"
    )
    aggregation: str = Field(default="avg", description="Tipo de agregação")


class MetricTrendData(BaseModel):
    """Schema para dados de tendência de métricas."""

    metric_id: UUID
    metric_name: str
    data_points: List[Dict[str, Any]]
    trend_direction: str = Field(
        ..., description="Direção da tendência (up, down, stable)"
    )
    trend_percentage: float = Field(..., description="Percentual de mudança")
    prediction_next_period: Optional[float] = None


class ExecutiveKPIs(BaseModel):
    """Schema para KPIs executivos principais."""

    total_users: int
    active_users_today: int
    total_documents: int
    documents_uploaded_today: int
    total_notifications: int
    notifications_sent_today: int
    system_uptime_percentage: float
    average_response_time_ms: float
    critical_alerts_count: int


class ModuleUsageStats(BaseModel):
    """Schema para estatísticas de uso por módulo."""

    module_name: str
    total_requests: int
    unique_users: int
    average_response_time: float
    error_rate: float
    top_endpoints: List[Dict[str, Any]]


class SystemPerformanceMetrics(BaseModel):
    """Schema para métricas de performance do sistema."""

    timestamp: datetime
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    database_connections: int
    active_sessions: int
    queue_size: int
    response_time_p95: float


class AnalyticsSummary(BaseModel):
    """Schema para resumo geral de analytics."""

    executive_kpis: ExecutiveKPIs
    module_usage: List[ModuleUsageStats]
    system_performance: SystemPerformanceMetrics
    top_trends: List[MetricTrendData]
    active_alerts: List[AlertRead]
    generated_at: datetime


class ChartConfiguration(BaseModel):
    """Schema para configuração de gráficos."""

    chart_type: str = Field(..., description="Tipo de gráfico (line, bar, pie, area)")
    title: str = Field(..., description="Título do gráfico")
    x_axis_label: Optional[str] = Field(None, description="Label do eixo X")
    y_axis_label: Optional[str] = Field(None, description="Label do eixo Y")
    show_legend: bool = Field(True, description="Mostrar legenda")
    colors: List[str] = Field(default_factory=list, description="Cores personalizadas")


class DashboardWidget(BaseModel):
    """Schema para widgets de dashboard."""

    widget_id: str = Field(..., description="ID único do widget")
    widget_type: str = Field(..., description="Tipo do widget (metric, chart, table)")
    title: str = Field(..., description="Título do widget")
    position: Dict[str, int] = Field(
        ..., description="Posição no dashboard (x, y, width, height)"
    )
    configuration: Dict[str, Any] = Field(
        ..., description="Configuração específica do widget"
    )
    data_source: Dict[str, Any] = Field(..., description="Fonte de dados")


class ExportConfiguration(BaseModel):
    """Schema para configuração de exportação."""

    format: ReportFormat = Field(..., description="Formato de saída")
    include_charts: bool = Field(True, description="Incluir gráficos")
    include_raw_data: bool = Field(False, description="Incluir dados brutos")
    compression_level: int = Field(
        default=6, ge=0, le=9, description="Nível de compressão (0-9)"
    )
    password_protected: bool = Field(False, description="Proteger com senha")
    custom_filename: Optional[str] = Field(
        None, description="Nome personalizado do arquivo"
    )


class ScheduledReportBase(BaseModel):
    """Schema base para relatórios agendados."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="Nome do relatório agendado"
    )
    report_type: ReportType = Field(..., description="Tipo do relatório")
    schedule_cron: str = Field(..., description="Expressão cron para agendamento")
    recipients: List[str] = Field(
        ..., min_length=1, description="Emails dos destinatários"
    )
    is_active: bool = Field(True, description="Se o agendamento está ativo")


class ScheduledReportCreate(ScheduledReportBase):
    """Schema para criação de relatórios agendados."""

    filters: Dict[str, Any] = Field(default_factory=dict, description="Filtros padrão")
    format: ReportFormat = Field(default=ReportFormat.PDF, description="Formato padrão")


class ScheduledReportRead(ScheduledReportBase):
    """Schema para leitura de relatórios agendados."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    last_executed_at: Optional[datetime] = None
    next_execution_at: Optional[datetime] = None
    execution_count: int = Field(0, description="Número de execuções")

    model_config = ConfigDict(from_attributes=True)
