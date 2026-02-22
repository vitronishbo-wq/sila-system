# apps/backend/modules/integration/schemas/cross_module_integration.py
"""Pydantic schemas para integração cross-module.

Modelos desenhados para serem claros, pequenos e reutilizáveis.
Compatível com Pydantic v2 (uso básico de BaseModel).
"""

from __future__ import annotations

from enum import Enum
from datetime import datetime, date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """Resposta genérica de API usada em endpoints simples."""

    success: bool = Field(..., description="Indica se a operação teve sucesso")
    message: Optional[str] = Field(None, description="Mensagem informativa / de erro")
    data: Optional[Any] = Field(None, description="Payload retornado pela API")


class PaginatedResponse(BaseModel):
    """Resposta paginada genérica."""

    items: List[Any] = Field(..., description="Lista de itens da página atual")
    total: int = Field(..., ge=0, description="Número total de itens")
    page: int = Field(..., ge=1, description="Página atual (1-based)")
    size: int = Field(
        ..., ge=1, description="Tamanho da página (número de itens por página)"
    )


class IntegrationSanitationIncident(BaseModel):
    """Incidente de saneamento reportado por integração entre módulos."""

    id: Optional[int] = Field(None, description="Identificador interno do incidente")
    external_id: Optional[str] = Field(
        None, description="Identificador externo fornecido pelo sistema origem"
    )
    reported_at: datetime = Field(
        ..., description="Timestamp de quando o incidente foi reportado"
    )
    location: Optional[str] = Field(
        None, description="Descrição textual da localização"
    )
    latitude: Optional[float] = Field(None, description="Latitude (se disponível)")
    longitude: Optional[float] = Field(None, description="Longitude (se disponível)")
    description: Optional[str] = Field(
        None, description="Descrição detalhada do incidente"
    )
    severity: Optional[str] = Field(
        None, description="Nível de severidade (ex: low, medium, high)"
    )
    status: Optional[str] = Field(
        None, description="Status atual do incidente (ex: open, closed)"
    )
    reporter: Optional[str] = Field(
        None, description="Nome ou identificação do reportante"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Campos adicionais/arbítrarios"
    )


class IntegrationSanitationStatistics(BaseModel):
    """Estatísticas agregadas para saneamento (úteis em dashboards)."""

    period_start: Optional[date] = Field(
        None, description="Data inicial do período das estatísticas"
    )
    period_end: Optional[date] = Field(
        None, description="Data final do período das estatísticas"
    )
    total_incidents: int = Field(0, ge=0, description="Total de incidentes no período")
    open_incidents: int = Field(0, ge=0, description="Incidentes atualmente abertos")
    closed_incidents: int = Field(0, ge=0, description="Incidentes já fechados")
    by_severity: Dict[str, int] = Field(
        default_factory=dict, description="Mapeamento severity -> quantidade"
    )
    by_location_bucket: Dict[str, int] = Field(
        default_factory=dict,
        description="Contagem agregada por área / distrito / bucket",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Campos adicionais/arbítrarios"
    )


class TechnicalResponsible(BaseModel):
    """Dados da pessoa técnica responsável por um item / integração."""

    id: Optional[int] = Field(None, description="Identificador interno do responsável")
    name: str = Field(..., description="Nome completo")
    email: Optional[str] = Field(None, description="E-mail de contacto")
    phone: Optional[str] = Field(
        None, description="Telefone de contacto (se aplicável)"
    )
    role: Optional[str] = Field(None, description="Cargo / função")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Campos adicionais/arbítrarios"
    )


class CrossModuleAlert(BaseModel):
    """Alerta simples que pode ser propagado entre módulos."""

    id: Optional[str] = Field(None, description="Identificador único do alerta")
    module: Optional[str] = Field(None, description="Módulo origem do alerta")
    title: str = Field(..., description="Título curto do alerta")
    message: Optional[str] = Field(None, description="Mensagem detalhada do alerta")
    severity: Optional[str] = Field(
        None, description="Nível do alerta (info, warning, critical)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp de criação"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Dados adicionais ligados ao alerta"
    )


class DashboardOverviewResponse(BaseModel):
    """Modelo de resposta usado em painéis de gestão / overview."""

    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Última actualização"
    )
    sanitation_statistics: Optional[IntegrationSanitationStatistics] = Field(
        None, description="Estatísticas agregadas de saneamento"
    )
    recent_alerts: List[CrossModuleAlert] = Field(
        default_factory=list, description="Alertas recentes"
    )
    quick_metrics: Optional[Dict[str, Any]] = Field(
        None, description="Métricas rápidas e customizáveis para o dashboard"
    )


class IntegrationReportResponse(BaseModel):
    """Estrutura de resposta para relatórios gerados por integrações."""

    report_id: Optional[str] = Field(None, description="Identificador do relatório")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp de geração"
    )
    summary: Optional[str] = Field(None, description="Resumo textual do relatório")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Conteúdo detalhado (estrutura arbitrária)"
    )
    download_url: Optional[str] = Field(
        None, description="URL para download do relatório (se aplicável)"
    )


class IntegrationStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IntegrationStatus(BaseModel):
    """Estado de uma integração / job."""

    external_id: Optional[str] = Field(
        None, description="ID externo do job/integration"
    )
    status: IntegrationStatusEnum = Field(..., description="Estado atual")
    last_updated: Optional[datetime] = Field(
        None, description="Última atualização conhecida"
    )
    message: Optional[str] = Field(None, description="Mensagem informativa ou de erro")
    progress: Optional[float] = Field(
        None, ge=0.0, le=100.0, description="Progresso percentual (0-100)"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Dados adicionais")


class IntegrationWorkflowRequest(BaseModel):
    """Pedido para disparar / orquestrar um workflow de integração entre módulos."""

    workflow_id: Optional[str] = Field(
        None, description="Identificador lógico do workflow"
    )
    module_name: str = Field(..., description="Nome do módulo alvo / responsável")
    action: str = Field(
        ..., description="Ação a executar (ex: 'sync', 'report', 'cleanup')"
    )
    payload: Optional[Dict[str, Any]] = Field(
        None, description="Dados arbitrários passados para o workflow"
    )
    requester_id: Optional[int] = Field(
        None, description="ID do utilizador que requisitou a ação"
    )
    requester: Optional[TechnicalResponsible] = Field(
        None, description="Dados do solicitante (se disponíveis)"
    )
    scheduled_at: Optional[datetime] = Field(
        None, description="Quando o workflow deverá ser executado (se agendado)"
    )
    priority: Optional[int] = Field(
        50, ge=0, le=100, description="Prioridade do workflow (0-100)"
    )
    notify: Optional[bool] = Field(
        False, description="Enviar notificação quando concluído"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Campos adicionais/arbítrarios"
    )
