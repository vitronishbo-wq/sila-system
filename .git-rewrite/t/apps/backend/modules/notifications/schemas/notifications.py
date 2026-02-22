"""
Schemas Pydantic para o módulo de Notificações.

Define estruturas de dados para sistema de notificações, incluindo:
- Gestão de notificações push, email e SMS
- Templates de mensagens personalizáveis
- Controle de entrega e confirmação de leitura
- Integração com eventos do sistema
- Relatórios de entrega e engajamento
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NotificationType(str, Enum):
    """Tipos de notificação disponíveis."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class NotificationPriority(str, Enum):
    """Níveis de prioridade das notificações."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class NotificationStatus(str, Enum):
    """Status de entrega das notificações."""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationChannel(str, Enum):
    """Canais de entrega disponíveis."""

    EMAIL = "email"
    SMS = "sms"
    PUSH_MOBILE = "push_mobile"
    PUSH_WEB = "push_web"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class NotificationTemplateBase(BaseModel):
    """Schema base para templates de notificação."""

    name: str = Field(..., min_length=1, max_length=255, description="Nome do template")
    description: str = Field(..., max_length=1000, description="Descrição do template")
    notification_type: NotificationType = Field(..., description="Tipo de notificação")
    subject: str = Field(
        ..., max_length=255, description="Assunto/título da notificação"
    )
    body: str = Field(..., description="Corpo da mensagem com variáveis")
    variables: Dict[str, str] = Field(
        default_factory=dict, description="Variáveis disponíveis no template"
    )
    is_active: bool = Field(True, description="Se o template está ativo")


class NotificationTemplateCreate(NotificationTemplateBase):
    """Schema para criação de templates."""


class NotificationTemplateRead(NotificationTemplateBase):
    """Schema para leitura de templates."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    usage_count: int = Field(0, description="Número de usos")

    model_config = ConfigDict(from_attributes=True)


class NotificationBase(BaseModel):
    """Schema base para notificações."""

    recipient_id: UUID = Field(..., description="ID do destinatário")
    recipient_email: Optional[str] = Field(None, description="Email alternativo")
    recipient_phone: Optional[str] = Field(None, description="Telefone alternativo")
    notification_type: NotificationType = Field(..., description="Tipo de notificação")
    priority: NotificationPriority = Field(
        NotificationPriority.NORMAL, description="Prioridade"
    )
    channels: List[NotificationChannel] = Field(
        ..., min_length=1, description="Canais de entrega"
    )
    scheduled_at: Optional[datetime] = Field(None, description="Agendamento para envio")


class NotificationCreate(NotificationBase):
    """Schema para criação de notificações."""

    template_id: Optional[UUID] = Field(None, description="ID do template a usar")
    subject: str = Field(..., max_length=255, description="Assunto personalizado")
    body: str = Field(..., description="Corpo da mensagem")
    variables: Dict[str, Any] = Field(
        default_factory=dict, description="Variáveis para template"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados adicionais"
    )


class NotificationBulkCreate(BaseModel):
    """Schema para criação em lote de notificações."""

    recipients: List[UUID] = Field(
        ..., min_length=1, description="Lista de destinatários"
    )
    template_id: UUID = Field(..., description="ID do template a usar")
    variables: Dict[str, Any] = Field(
        default_factory=dict, description="Variáveis para template"
    )
    channels: List[NotificationChannel] = Field(
        ..., min_length=1, description="Canais de entrega"
    )
    priority: NotificationPriority = Field(
        NotificationPriority.NORMAL, description="Prioridade"
    )
    scheduled_at: Optional[datetime] = Field(None, description="Agendamento para envio")


class NotificationUpdate(BaseModel):
    """Schema para atualização de notificações."""

    priority: Optional[NotificationPriority] = Field(
        None, description="Nova prioridade"
    )
    scheduled_at: Optional[datetime] = Field(None, description="Novo agendamento")
    channels: Optional[List[NotificationChannel]] = Field(
        None, description="Novos canais"
    )


class NotificationRead(NotificationBase):
    """Schema para leitura de notificações."""

    id: UUID
    template_id: Optional[UUID]
    template_name: Optional[str]
    subject: str
    body: str
    status: NotificationStatus
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    delivery_attempts: int = Field(0, description="Tentativas de entrega")
    metadata: Dict[str, Any]

    # Informações do remetente
    sent_by: UUID
    sent_by_name: str

    # Estatísticas de entrega
    email_delivered: bool = Field(False, description="Entregue por email")
    sms_delivered: bool = Field(False, description="Entregue por SMS")
    push_delivered: bool = Field(False, description="Entregue por push")

    model_config = ConfigDict(from_attributes=True)


class NotificationDeliveryBase(BaseModel):
    """Schema base para registros de entrega."""

    notification_id: UUID = Field(..., description="ID da notificação")
    channel: NotificationChannel = Field(..., description="Canal utilizado")
    provider: str = Field(
        ..., description="Provedor de entrega (SMTP, Twilio, FCM, etc.)"
    )
    provider_message_id: Optional[str] = Field(
        None, description="ID da mensagem no provedor"
    )
    status: NotificationStatus = Field(..., description="Status da entrega")
    error_message: Optional[str] = Field(
        None, description="Mensagem de erro se aplicável"
    )


class NotificationDeliveryCreate(NotificationDeliveryBase):
    """Schema para criação de registros de entrega."""

    delivered_at: Optional[datetime] = Field(None, description="Data/hora da entrega")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados da entrega"
    )


class NotificationDeliveryRead(NotificationDeliveryBase):
    """Schema para leitura de registros de entrega."""

    id: UUID
    delivered_at: Optional[datetime]
    metadata: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationEventBase(BaseModel):
    """Schema base para eventos que disparam notificações."""

    event_type: str = Field(..., description="Tipo do evento")
    entity_type: str = Field(..., description="Tipo da entidade relacionada")
    entity_id: UUID = Field(..., description="ID da entidade")
    trigger_data: Dict[str, Any] = Field(
        default_factory=dict, description="Dados do trigger"
    )
    recipient_filters: Dict[str, Any] = Field(
        default_factory=dict, description="Filtros para destinatários"
    )


class NotificationEventCreate(NotificationEventBase):
    """Schema para criação de eventos."""

    priority: NotificationPriority = Field(
        NotificationPriority.NORMAL, description="Prioridade do evento"
    )


class NotificationEventRead(NotificationEventBase):
class NotificationEventRead(NotificationEventBase):
    """Schema para leitura de eventos."""

    id: UUID
    created_by: UUID
    created_at: datetime
    processed_at: Optional[datetime] = None
    notifications_sent: int = Field(0, description="Número de notificações enviadas")

    model_config = ConfigDict(from_attributes=True)

class NotificationSettingsBase(BaseModel):
    """Schema base para configurações de notificação do usuário."""

    email_notifications: bool = Field(
        True, description="Receber notificações por email"
    )
    sms_notifications: bool = Field(False, description="Receber notificações por SMS")
    push_notifications: bool = Field(True, description="Receber notificações push")
    in_app_notifications: bool = Field(True, description="Receber notificações in-app")
    notification_frequency: str = Field(
        "immediate", description="Frequência de notificações"
    )
    quiet_hours_start: Optional[str] = Field(
        None, description="Início do período de silêncio"
    )
    quiet_hours_end: Optional[str] = Field(
        None, description="Fim do período de silêncio"
    )


class NotificationSettingsCreate(NotificationSettingsBase):
    """Schema para criação de configurações."""

    user_id: UUID = Field(..., description="ID do usuário")


class NotificationSettingsRead(NotificationSettingsBase):
class NotificationSettingsRead(NotificationSettingsBase):
    """Schema para leitura de configurações."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationStatistics(BaseModel):
    """Schema para estatísticas de notificações."""

    total_notifications: int
    notifications_by_type: Dict[str, int]
    notifications_by_status: Dict[str, int]
    notifications_by_channel: Dict[str, int]
    delivery_rate: float
    read_rate: float
    average_delivery_time_seconds: float
    top_templates: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]


class NotificationQueueItemBase(BaseModel):
    """Schema base para itens na fila de notificações."""

    notification_id: UUID = Field(..., description="ID da notificação")
    priority: int = Field(..., ge=1, le=10, description="Prioridade na fila (1-10)")
    scheduled_for: datetime = Field(..., description="Data/hora agendada para envio")
    retry_count: int = Field(0, description="Número de tentativas de reenvio")
    max_retries: int = Field(3, description="Número máximo de tentativas")


class NotificationQueueItemRead(NotificationQueueItemBase):
class NotificationQueueItemRead(NotificationQueueItemBase):
    """Schema para leitura de itens da fila."""

    id: UUID
    created_at: datetime
    last_attempt_at: Optional[datetime] = None
    next_retry_at: Optional[datetime] = None
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class NotificationWebhookBase(BaseModel):
    """Schema base para configurações de webhook."""

    url: str = Field(..., description="URL do webhook")
    secret: str = Field(..., description="Chave secreta para validação")
    events: List[str] = Field(..., min_length=1, description="Eventos a serem enviados")
    is_active: bool = Field(True, description="Se o webhook está ativo")
    retry_on_failure: bool = Field(
        True, description="Tentar novamente em caso de falha"
    )


class NotificationWebhookCreate(NotificationWebhookBase):
    """Schema para criação de webhooks."""

    name: str = Field(..., min_length=1, max_length=255, description="Nome do webhook")


class NotificationWebhookRead(NotificationWebhookBase):
    """Schema para leitura de webhooks."""
class NotificationWebhookRead(NotificationWebhookBase):
    """Schema para leitura de webhooks."""

    id: UUID
    name: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    last_triggered_at: Optional[datetime] = None
    success_count: int = Field(0, description="Número de sucessos")
    failure_count: int = Field(0, description="Número de falhas")

    model_config = ConfigDict(from_attributes=True)
class NotificationAlertBase(BaseModel):
    """Schema base para alertas do sistema."""

    alert_type: str = Field(..., description="Tipo do alerta")
    severity: str = Field(
        ..., description="Severidade (info, warning, error, critical)"
    )
    title: str = Field(..., max_length=255, description="Título do alerta")
    message: str = Field(..., description="Mensagem detalhada")
    affected_systems: List[str] = Field(
        default_factory=list, description="Sistemas afetados"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados adicionais"
    )


class NotificationAlertCreate(NotificationAlertBase):
    """Schema para criação de alertas."""

    expires_at: Optional[datetime] = Field(
        None, description="Data de expiração do alerta"
    )


class NotificationAlertRead(NotificationAlertBase):
    """Schema para leitura de alertas."""
class NotificationAlertRead(NotificationAlertBase):
    """Schema para leitura de alertas."""

    id: UUID
    created_by: UUID
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool = Field(True, description="Se o alerta está ativo")
    acknowledged_by: List[UUID] = Field(
        default_factory=list, description="Usuários que reconheceram"
    )

    model_config = ConfigDict(from_attributes=True)
class NotificationFilters(BaseModel):
    """Schema para filtros de busca de notificações."""

    notification_type: Optional[NotificationType] = None
    status: Optional[NotificationStatus] = None
    priority: Optional[NotificationPriority] = None
    channel: Optional[NotificationChannel] = None
    recipient_id: Optional[UUID] = None
    template_id: Optional[UUID] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    read_status: Optional[bool] = None


class NotificationBulkOperation(BaseModel):
    """Schema para operações em lote."""

    notification_ids: List[UUID] = Field(
        ..., min_length=1, description="IDs das notificações"
    )
    operation: str = Field(
        ..., description="Operação (mark_read, mark_unread, cancel, retry)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados da operação"
    )


class NotificationReportFilters(BaseModel):
    """Schema para filtros de relatórios."""

    period_start: datetime = Field(..., description="Início do período")
    period_end: datetime = Field(..., description="Fim do período")
    notification_types: List[NotificationType] = Field(
        default_factory=list, description="Tipos de notificação"
    )
    channels: List[NotificationChannel] = Field(
        default_factory=list, description="Canais de entrega"
    )
    user_groups: List[str] = Field(
        default_factory=list, description="Grupos de usuários"
    )


class NotificationReportRead(BaseModel):
    """Schema para leitura de relatórios."""

    period_start: datetime
    period_end: datetime
    total_notifications: int
    notifications_by_type: Dict[str, int]
    notifications_by_channel: Dict[str, int]
    notifications_by_status: Dict[str, int]
    delivery_success_rate: float
    average_delivery_time: float
    top_performing_templates: List[Dict[str, Any]]
    user_engagement_metrics: Dict[str, Any]
