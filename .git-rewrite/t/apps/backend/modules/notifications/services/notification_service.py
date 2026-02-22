"""
Serviço principal para gestão de notificações.

Este módulo implementa a lógica de negócio completa para:
- Envio multicanal de notificações (email, SMS, push, in-app)
- Gestão de templates reutilizáveis
- Controle de fila e agendamento
- Eventos automáticos baseados em triggers
- Webhooks para integração externa
- Relatórios e métricas de entrega
- Configurações personalizadas por usuário
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

try:
    import aiohttp
except Exception:
    aiohttp = None
from sqlalchemy import desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.citizenship.models.citizen import Citizen
from modules.notifications.models.notification_models import (
    Notification,
    NotificationQueue,
    NotificationSettings,
    NotificationTemplate,
)
from modules.notifications.schemas.notifications import (
    NotificationCreate,
    NotificationFilters,
    NotificationRead,
    NotificationStatistics,
)

logger = logging.getLogger(__name__)

# Configurações de serviço
MAX_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 60  # segundos
BATCH_SIZE = 50  # notificações por lote


class NotificationService:
    """Classe principal para operações de notificações."""

    @staticmethod
    async def create_notification(
        db: AsyncSession, notification_data: NotificationCreate, sender_id: UUID
    ) -> NotificationRead:
        """
        Cria nova notificação individual.

        Args:
            db: Sessão do banco de dados
            notification_data: Dados da notificação
            sender_id: ID do usuário que está enviando

        Returns:
            Notificação criada
        """
        try:
            # Buscar template se especificado
            template = None
            if notification_data.template_id:
                template = (
                    db.query(NotificationTemplate)
                    .filter(
                        NotificationTemplate.id == notification_data.template_id,
                        NotificationTemplate.is_active == True,
                    )
                    .first()
                )

                if not template:
                    raise ValueError("Template não encontrado ou inativo")

            # Buscar configurações do destinatário
            recipient_settings = (
                db.query(NotificationSettings)
                .filter(NotificationSettings.user_id == notification_data.recipient_id)
                .first()
            )

            # Verificar se canais estão habilitados para o destinatário
            enabled_channels = []
            if recipient_settings:
                if (
                    recipient_settings.email_notifications
                    and NotificationChannel.EMAIL in notification_data.channels
                ):
                    enabled_channels.append(NotificationChannel.EMAIL)
                if (
                    recipient_settings.sms_notifications
                    and NotificationChannel.SMS in notification_data.channels
                ):
                    enabled_channels.append(NotificationChannel.SMS)
                if (
                    recipient_settings.push_notifications
                    and NotificationChannel.PUSH_WEB in notification_data.channels
                ):
                    enabled_channels.append(NotificationChannel.PUSH_WEB)
                if (
                    recipient_settings.in_app_notifications
                    and NotificationChannel.IN_APP in notification_data.channels
                ):
                    enabled_channels.append(NotificationChannel.IN_APP)
            else:
                # Se não há configurações, usar canais padrão
                enabled_channels = notification_data.channels

            if not enabled_channels:
                raise ValueError("Nenhum canal habilitado para o destinatário")

            # Processar template se aplicável
            subject, body = await NotificationService._process_template(
                template,
                notification_data.variables,
                notification_data.subject,
                notification_data.body,
            )

            # Criar notificação
            new_notification = Notification(
                recipient_id=notification_data.recipient_id,
                recipient_email=notification_data.recipient_email,
                recipient_phone=notification_data.recipient_phone,
                template_id=notification_data.template_id,
                notification_type=notification_data.notification_type,
                priority=notification_data.priority,
                subject=subject,
                body=body,
                channels=enabled_channels,
                scheduled_at=notification_data.scheduled_at,
                variables=notification_data.variables,
                metadata=notification_data.metadata,
                sent_by=sender_id,
            )

            db.add(new_notification)

            # Se agendada para envio imediato, adicionar à fila
            if (
                not notification_data.scheduled_at
                or notification_data.scheduled_at <= datetime.utcnow()
            ):
                queue_item = NotificationQueue(
                    notification_id=new_notification.id,
                    priority=NotificationService._priority_to_int(
                        notification_data.priority
                    ),
                    scheduled_for=datetime.utcnow(),
                )
                db.add(queue_item)

            db.commit()
            db.refresh(new_notification)

            # Atualizar contador de uso do template
            if template:
                template.usage_count += 1
                db.commit()

            # Converter para schema de leitura
            notification_dict = await NotificationService._notification_to_dict(
                db, new_notification
            )

            logger.info(f"Notificação criada: {new_notification.id}")
            return NotificationRead(**notification_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar notificação: {e}")
            raise

    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id: UUID,
        filters: Optional[NotificationFilters] = None,
        page: int = 1,
        size: int = 20,
    ) -> Tuple[List[NotificationRead], int]:
        """
        Busca notificações do usuário.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            filters: Filtros opcionais
            page: Página para paginação
            size: Tamanho da página

        Returns:
            Tupla com notificações e total
        """
        try:
            query = (
                db.query(Notification)
                .options(
                    selectinload(Notification.template),
                    selectinload(Notification.sender),
                )
                .filter(Notification.recipient_id == user_id)
            )

            # Aplicar filtros
            if filters:
                if filters.notification_type:
                    query = query.filter(
                        Notification.notification_type == filters.notification_type
                    )
                if filters.status:
                    query = query.filter(Notification.status == filters.status)
                if filters.priority:
                    query = query.filter(Notification.priority == filters.priority)
                if filters.template_id:
                    query = query.filter(
                        Notification.template_id == filters.template_id
                    )
                if filters.date_from:
                    query = query.filter(Notification.created_at >= filters.date_from)
                if filters.date_to:
                    query = query.filter(Notification.created_at <= filters.date_to)
                if filters.read_status is not None:
                    if filters.read_status:
                        query = query.filter(Notification.read_at.isnot(None))
                    else:
                        query = query.filter(Notification.read_at.is_(None))

            total = query.count()
            notifications = (
                query.order_by(desc(Notification.created_at))
                .offset((page - 1) * size)
                .limit(size)
                .all()
            )

            # Converter para schema de leitura
            result = []
            for notification in notifications:
                notification_dict = await NotificationService._notification_to_dict(
                    db, notification
                )
                result.append(NotificationRead(**notification_dict))

            return result, total

        except Exception as e:
            logger.error(f"Erro ao buscar notificações do usuário: {e}")
            raise

    @staticmethod
    async def mark_notification_read(
        db: AsyncSession, notification_id: UUID, user_id: UUID
    ) -> bool:
        """
        Marca notificação como lida.

        Args:
            db: Sessão do banco de dados
            notification_id: ID da notificação
            user_id: ID do usuário

        Returns:
            True se marcada com sucesso
        """
        try:
            notification = (
                db.query(Notification)
                .filter(
                    Notification.id == notification_id,
                    Notification.recipient_id == user_id,
                )
                .first()
            )

            if not notification:
                return False

            if not notification.read_at:
                notification.read_at = datetime.utcnow()
                notification.status = "read"
                db.commit()

                # Registrar evento
                await NotificationService._log_user_action(
                    db,
                    user_id,
                    "notification_read",
                    {"notification_id": str(notification_id)},
                )

            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao marcar notificação como lida: {e}")
            raise

    @staticmethod
    async def get_notification_statistics(
        db: AsyncSession, user_id: UUID
    ) -> NotificationStatistics:
        """
        Obtém estatísticas de notificações do usuário.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário

        Returns:
            Estatísticas detalhadas
        """
        try:
            # Query base
            base_query = db.query(Notification).filter(
                Notification.recipient_id == user_id
            )

            # Estatísticas gerais
            total_notifications = base_query.count()
            notifications_by_type = dict(
                base_query.with_entities(
                    Notification.notification_type, func.count(Notification.id)
                )
                .group_by(Notification.notification_type)
                .all()
            )

            notifications_by_status = dict(
                base_query.with_entities(
                    Notification.status, func.count(Notification.id)
                )
                .group_by(Notification.status)
                .all()
            )

            # Estatísticas de entrega
            delivered_count = base_query.filter(
                Notification.status == "delivered"
            ).count()
            read_count = base_query.filter(Notification.read_at.isnot(None)).count()

            delivery_rate = (delivered_count / max(total_notifications, 1)) * 100
            read_rate = (
                (read_count / max(delivered_count, 1)) * 100
                if delivered_count > 0
                else 0
            )

            # Tempo médio de entrega (simplificado)
            avg_delivery_time = 0  # Implementar quando necessário

            # Templates mais usados (simplificado)
            top_templates = []

            # Atividade recente (últimas 10)
            recent_activity = (
                base_query.order_by(desc(Notification.created_at)).limit(10).all()
            )
            recent_list = [
                {
                    "id": str(n.id),
                    "type": n.notification_type.value,
                    "subject": n.subject,
                    "status": n.status.value,
                    "created_at": n.created_at.isoformat(),
                }
                for n in recent_activity
            ]

            return NotificationStatistics(
                total_notifications=total_notifications,
                notifications_by_type=notifications_by_type,
                notifications_by_status=notifications_by_status,
                notifications_by_channel={},  # Implementar quando necessário
                delivery_rate=delivery_rate,
                read_rate=read_rate,
                average_delivery_time_seconds=avg_delivery_time,
                top_templates=top_templates,
                recent_activity=recent_list,
            )

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise

    # Métodos auxiliares privados

    @staticmethod
    async def _process_template(
        template: Optional[NotificationTemplate],
        variables: Dict[str, Any],
        fallback_subject: str,
        fallback_body: str,
    ) -> Tuple[str, str]:
        """Processa template com variáveis."""
        if not template:
            return fallback_subject, fallback_body

        subject = template.subject
        body = template.body

        # Substituir variáveis
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))

        return subject, body

    @staticmethod
    def _priority_to_int(priority: str) -> int:
        """Converte prioridade string para int (1-10)."""
        priority_map = {"low": 2, "normal": 5, "high": 8, "urgent": 9, "critical": 10}
        return priority_map.get(priority, 5)

    @staticmethod
    async def _notification_to_dict(
        db: AsyncSession, notification: Notification
    ) -> Dict[str, Any]:
        """Converte modelo Notification para dicionário."""
        # Buscar remetente
        sender = db.query(Citizen).filter(Citizen.id == notification.sent_by).first()

        # Buscar template se aplicável
        template_name = None
        if notification.template_id:
            template = (
                db.query(NotificationTemplate)
                .filter(NotificationTemplate.id == notification.template_id)
                .first()
            )
            template_name = template.name if template else None

        return {
            "id": notification.id,
            "recipient_id": notification.recipient_id,
            "recipient_email": notification.recipient_email,
            "recipient_phone": notification.recipient_phone,
            "notification_type": notification.notification_type,
            "priority": notification.priority,
            "channels": notification.channels,
            "scheduled_at": notification.scheduled_at,
            "template_id": notification.template_id,
            "template_name": template_name,
            "subject": notification.subject,
            "body": notification.body,
            "status": notification.status,
            "sent_at": notification.sent_at,
            "delivered_at": notification.delivered_at,
            "read_at": notification.read_at,
            "failed_at": notification.failed_at,
            "error_message": notification.error_message,
            "delivery_attempts": notification.delivery_attempts,
            "metadata": notification.metadata or {},
            "sent_by": notification.sent_by,
            "sent_by_name": sender.full_name if sender else "Sistema",
            "email_delivered": notification.email_delivered,
            "sms_delivered": notification.sms_delivered,
            "push_delivered": notification.push_delivered,
        }

    @staticmethod
    async def _log_user_action(
        db: AsyncSession,
        user_id: UUID,
        action: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Registra ação do usuário para auditoria."""
        logger.info(f"Ação do usuário registrada: {user_id} - {action}")
