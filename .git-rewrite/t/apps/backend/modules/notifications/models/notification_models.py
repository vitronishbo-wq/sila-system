"""
Modelos SQLAlchemy para o módulo de Notificações.

Define as entidades principais para:
- Gestão completa de notificações multicanal
- Templates reutilizáveis de mensagens
- Controle de entrega e rastreamento
- Eventos automáticos e webhooks
- Configurações personalizadas por usuário
- Auditoria e relatórios detalhados
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import backref, relationship

from core.db.base_class import Base  # Use centralized Base

from ..schemas.notifications import (
    NotificationChannel,
    NotificationPriority,
    NotificationStatus,
    NotificationType,
)

# Remove local Base creation


class NotificationTemplate(Base):
    """
    Modelo para templates reutilizáveis de notificações.

    Permite criar mensagens padronizadas que podem ser
    reutilizadas com variáveis personalizadas.
    """

    __tablename__ = "notifications_notification_templates"

    __table_args__ = {"extend_existing": True}

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    variables = Column(JSON)  # Campos variáveis disponíveis
    is_active = Column(Boolean, default=True, nullable=False)

    # Controle de uso
    usage_count = Column(Integer, default=0, nullable=False)

    # Controle de acesso
    created_by = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
    )
    is_public = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("notification_templates", lazy="dynamic"),
    )
    notifications = relationship(
        "Notification",
        foreign_keys="[Notification.template_id]",
        back_populates="template",
    )

    def __repr__(self):
        return f"<NotificationTemplate(id={self.id}, name='{self.name}', type={self.notification_type})>"


class Notification(Base):
    """
    Modelo principal para notificações individuais.

    Controla todas as notificações enviadas no sistema,
    incluindo múltiplos canais de entrega e rastreamento.
    """

    __tablename__ = "notifications_notifications"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Destinatário
    recipient_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
        index=True,
    )
    recipient_email = Column(String(255))
    recipient_phone = Column(String(20))

    # Relacionamentos
    template_id = Column(
        PGUUID(as_uuid=True), ForeignKey("notification_templates.id")
    )

    # Dados da notificação
    notification_type = Column(Enum(NotificationType), nullable=False, index=True)
    priority = Column(
        Enum(NotificationPriority), default=NotificationPriority.NORMAL, nullable=False
    )
    status = Column(
        Enum(NotificationStatus),
        default=NotificationStatus.PENDING,
        nullable=False,
        index=True,
    )
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    variables = Column(JSON)  # Variáveis substituídas no template

    # Canais de entrega
    channels = Column(JSON, nullable=False)  # Lista de canais selecionados

    # Controle de entrega
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    failed_at = Column(DateTime)
    error_message = Column(Text)

    # Tentativas de entrega
    delivery_attempts = Column(Integer, default=0, nullable=False)

    # Controle de entrega por canal
    email_delivered = Column(Boolean, default=False, nullable=False)
    sms_delivered = Column(Boolean, default=False, nullable=False)
    push_delivered = Column(Boolean, default=False, nullable=False)

    # Metadados
    extra_data = Column(JSON, name="metadata")

    # Controle de acesso
    sent_by = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    recipient = relationship(
        "Citizen",
        foreign_keys=[recipient_id],
        backref=backref("received_notifications", lazy="dynamic"),
    )
    template = relationship(
        "NotificationTemplate",
        foreign_keys="[template_id]",
        back_populates="notifications",
    )
    sender = relationship(
        "Citizen",
        foreign_keys=[sent_by],
        backref=backref("sent_notifications", lazy="dynamic"),
    )
    deliveries = relationship(
        "NotificationDelivery",
        back_populates="notification",
        cascade="all, delete-orphan",
    )
    events = relationship(
        "NotificationEvent", back_populates="notification", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.notification_type}, status={self.status})>"


class NotificationDelivery(Base):
    """
    Modelo para rastreamento detalhado de entrega.

    Registra cada tentativa de entrega por canal,
    incluindo sucesso, falha e metadados específicos.
    """

    __tablename__ = "notifications_notification_deliveries"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    notification_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("notifications_notifications.id"),
        nullable=False,
    )

    # Dados da entrega
    channel = Column(Enum(NotificationChannel), nullable=False, index=True)
    provider = Column(String(100), nullable=False)  # SMTP, Twilio, FCM, etc.
    provider_message_id = Column(String(255))  # ID único do provedor
    status = Column(Enum(NotificationStatus), nullable=False, index=True)

    # Controle de tempo
    delivered_at = Column(DateTime)
    error_message = Column(Text)

    # Metadados específicos do canal
    extra_data = Column(JSON, name="metadata")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    notification = relationship(
        "Notification", foreign_keys=[notification_id], back_populates="deliveries"
    )

    def __repr__(self):
        return f"<NotificationDelivery(id={self.id}, channel={self.channel}, status={self.status})>"


class NotificationEvent(Base):
    """
    Modelo para eventos que disparam notificações automáticas.

    Define regras de negócio para envio automático de notificações
    baseado em eventos do sistema.
    """

    __tablename__ = "notifications_notification_events"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    notification_id = Column(
        PGUUID(as_uuid=True), ForeignKey("notifications_notifications.id")
    )

    # Dados do evento
    event_type = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    trigger_data = Column(JSON)  # Dados que dispararam o evento
    recipient_filters = Column(JSON)  # Filtros para determinar destinatários

    # Controle de processamento
    processed_at = Column(DateTime)
    notifications_sent = Column(Integer, default=0, nullable=False)

    # Controle de acesso
    created_by = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos
    notification = relationship(
        "Notification", foreign_keys=[notification_id], back_populates="events"
    )
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("notification_events", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<NotificationEvent(id={self.id}, type={self.event_type}, entity={self.entity_type})>"


class NotificationSettings(Base):
    """
    Modelo para configurações personalizadas de notificação.

    Permite que cada usuário configure suas preferências
    de recebimento de notificações por canal.
    """

    __tablename__ = "notifications_notification_settings"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    user_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
        unique=True,
    )

    # Configurações por canal
    email_notifications = Column(Boolean, default=True, nullable=False)
    sms_notifications = Column(Boolean, default=False, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)
    in_app_notifications = Column(Boolean, default=True, nullable=False)

    # Controle de frequência
    notification_frequency = Column(
        String(50), default="immediate", nullable=False
    )  # immediate, daily, weekly
    quiet_hours_start = Column(String(5))  # Formato HH:MM
    quiet_hours_end = Column(String(5))  # Formato HH:MM

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    user = relationship(
        "Citizen", backref=backref("notification_settings", uselist=False)
    )

    def __repr__(self):
        return f"<NotificationSettings(id={self.id}, user_id={self.user_id})>"


class NotificationQueue(Base):
    """
    Modelo para fila de processamento de notificações.

    Gerencia notificações agendadas e garante entrega
    confiável mesmo em caso de falhas temporárias.
    """

    __tablename__ = "notifications_notification_queue"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    notification_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("notifications_notifications.id"),
        nullable=False,
        unique=True,
    )

    # Controle de prioridade e agendamento
    priority = Column(
        Integer, default=5, nullable=False
    )  # 1-10, sendo 10 mais prioritário
    scheduled_for = Column(DateTime, nullable=False, index=True)

    # Controle de retentativas
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    last_attempt_at = Column(DateTime)
    next_retry_at = Column(DateTime)
    error_message = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    notification = relationship(
        "Notification", backref=backref("queue_item", uselist=False)
    )

    def __repr__(self):
        return f"<NotificationQueue(id={self.id}, notification_id={self.notification_id}, priority={self.priority})>"


class NotificationWebhook(Base):
    """
    Modelo para configurações de webhook externo.

    Permite integração com sistemas externos via HTTP callbacks
    para eventos específicos de notificações.
    """

    __tablename__ = "notifications_notification_webhooks"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Dados básicos
    name = Column(String(255), nullable=False, index=True)
    url = Column(String(1000), nullable=False)
    secret = Column(String(255), nullable=False)  # Para validação de segurança

    # Configurações
    events = Column(JSON, nullable=False)  # Lista de eventos a monitorar
    is_active = Column(Boolean, default=True, nullable=False)
    retry_on_failure = Column(Boolean, default=True, nullable=False)

    # Estatísticas
    success_count = Column(Integer, default=0, nullable=False)
    failure_count = Column(Integer, default=0, nullable=False)
    last_triggered_at = Column(DateTime)

    # Controle de acesso
    created_by = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("notification_webhooks", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<NotificationWebhook(id={self.id}, name='{self.name}', url='{self.url[:50]}...')>"


class NotificationAlert(Base):
    """
    Modelo para alertas críticos do sistema.

    Gerencia alertas importantes que precisam ser
    comunicados urgentemente aos usuários ou administradores.
    """

    __tablename__ = "notifications_notification_alerts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Dados do alerta
    alert_type = Column(String(100), nullable=False, index=True)
    severity = Column(
        String(20), nullable=False, index=True
    )  # info, warning, error, critical
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    affected_systems = Column(JSON)  # Lista de sistemas afetados
    extra_data = Column(JSON, name="metadata")  # Dados adicionais do alerta

    # Controle de expiração
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)

    # Controle de reconhecimento
    acknowledged_by = Column(JSON)  # Lista de UUIDs de usuários que reconheceram

    # Controle de acesso
    created_by = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("notification_alerts", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<NotificationAlert(id={self.id}, type={self.alert_type}, severity={self.severity})>"


# Índices adicionais para otimização de consultas
from sqlalchemy import Index

# Índices compostos para consultas frequentes
Index(
    "idx_notifications_recipient_status", Notification.recipient_id, Notification.status
)
Index(
    "idx_notifications_type_priority",
    Notification.notification_type,
    Notification.priority,
)
Index("idx_notifications_scheduled_at", Notification.scheduled_at)

Index(
    "idx_deliveries_notification_channel",
    NotificationDelivery.notification_id,
    NotificationDelivery.channel,
)
Index(
    "idx_deliveries_status_provider",
    NotificationDelivery.status,
    NotificationDelivery.provider,
)

Index(
    "idx_events_type_entity",
    NotificationEvent.event_type,
    NotificationEvent.entity_type,
)
Index("idx_events_processed_at", NotificationEvent.processed_at)

Index(
    "idx_queue_scheduled_priority",
    NotificationQueue.scheduled_for,
    NotificationQueue.priority,
)
Index("idx_queue_next_retry", NotificationQueue.next_retry_at)

Index(
    "idx_templates_type_active",
    NotificationTemplate.notification_type,
    NotificationTemplate.is_active,
)
Index("idx_templates_created_by", NotificationTemplate.created_by)

Index(
    "idx_webhooks_active_events",
    NotificationWebhook.is_active,
    NotificationWebhook.events,
)
Index("idx_webhooks_created_by", NotificationWebhook.created_by)

Index(
    "idx_alerts_severity_active",
    NotificationAlert.severity,
    NotificationAlert.is_active,
)
Index("idx_alerts_expires_at", NotificationAlert.expires_at)
